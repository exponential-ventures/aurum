#!/usr/bin/env python3
##
## Authors: Adriano Marques
##          Nathan Martins
##          Thales Ribeiro
##
## Copyright (C) 2019 Exponential Ventures LLC
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##

__author__ = "Adriano Marques, Nathan Martins, Thales Ribeiro"
__copyright__ = "Copyright (C) 2019 Exponential Ventures LLC"
__license__ = "GNU LESSER GENERAL PUBLIC LICENSE 2.0"
__url__ = "https://github.com/exponential-ventures/aurum"
__version__ = "0.1"

import argparse
import logging
import os
import shutil
import sys

from aurum import constants as cons, base
from aurum import git
from aurum.metadata import get_dataset_metadata, DatasetMetaData, load_parameters
from aurum.utils import make_safe_filename, check_inside_au
from aurum.singleton import SingletonDecorator


@SingletonDecorator
class Parser:
    def __init__(self):
        check_inside_au()

        description = """Aurum is a new and simplified approach for data scientists to
        keep track of data and code without having to get another PhD for it. Aurum
        keeps track of all code and data changes, and lets you easily reproduce any
        experiment as well as easily compare metrics across experiments.
        """
        epilog = "And that's how you make your live easier. You're welcome."
        self.parser = argparse.ArgumentParser(description=description, epilog=epilog, add_help=True)

        self.parser.add_argument('-v', '--verbose', required=False, default=False)
        self.parser.add_argument('-d', '--dry-run', required=False, default=False)

        try:
            known_params = load_parameters()
        except FileNotFoundError:
            known_params = {}

        for param in known_params.keys():
            self.parser.add_argument(f'-{param}', required=False, default=known_params[param])

        self.parse_args()

        # TODO: Save preference on verbose or dry run into the instance for easy access

    def parse_args(self):
        self.known_params, self.unknown_params = self.parser.parse_known_args()


parser = Parser()


@SingletonDecorator
class VersionTheorem:
    """
    Singleton class responsible act as a single source of truth regarding the experiment change's state
    Eg. inform that the source-code has changed
    """

    def __init__(self):
        self.requirements_changed = False
        self.code_changed = False
        self.dataset_changed = False
        self.parameters_changed = False

    def has_any_change(self):
        return self.requirements_changed or self.code_changed or self.dataset_changed or self.parameters_changed \
               or self.metrics_changed

    def requirements_did_change(self, requirements_metadata_location_hash: str) -> None:
        self.requirements_changed = requirements_metadata_location_hash

    def code_did_change(self, code_metadata_location_hash: str) -> None:
        self.code_changed = code_metadata_location_hash

    def dataset_did_change(self, dataset_metadata_location_hash: str) -> None:
        self.dataset_changed = dataset_metadata_location_hash

    def parameters_did_change(self, parameters_metadata_location_hash: str) -> None:
        self.parameters_changed = parameters_metadata_location_hash


init = VersionTheorem()


def run_init(parser: argparse.Namespace) -> None:
    logging.info("Initializing git...")
    git.init()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug(f"Repository {base.cwd} initialized.")


def run_add(parser: argparse.Namespace) -> None:
    for f in parser.files:

        full_f = os.path.join(os.getcwd(), f)
        f = check_file(f)

        mdf = DatasetMetaData()
        mdf.file_name = f
        mdf.size = os.path.getsize(full_f)
        meta_data_file_name = mdf.save()

        git_proc = git.run_git("add", full_f, meta_data_file_name, )

        result = git_proc.wait()

        if result != 0:
            message = f"Unable to run 'git add {meta_data_file_name} {f}' Exit code: {result}\n"
            if git_proc.stderr:
                message += f"{git_proc.stderr.read()}\n"

            logging.error(message)
            sys.exit(1)

    sys.stdout.write(f"Added: {parser.files}\n")


def run_rm(parser) -> None:
    for filepath in parser.files:

        filepath = check_file(filepath)

        logging.info(f"Removing {filepath} from git")
        git.rm(filepath, soft_delete=parser.soft_delete)
        logging.info(f"{filepath} removed from git")

        meta_data_path, _ = get_dataset_metadata(filepath)

        if meta_data_path:

            logging.info(f"Removing meta data '{meta_data_path}' and removing from git.")

            git.rm(meta_data_path, soft_delete=parser.soft_delete)

            # might have been removed by git, might not.
            if os.path.exists(meta_data_path):
                os.remove(meta_data_path)

            # remove parent dir if empty to avoid lots of empty dirs.
            parent_dir = os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR, make_safe_filename(filepath))
            if len(os.listdir(parent_dir)) <= 1:
                shutil.rmtree(parent_dir, ignore_errors=True)

            logging.info(f"Removed meta data '{meta_data_path}' and removed from git.")

        else:
            logging.warning(f"Unable to find metadata for file: '{filepath}' ")


def create_default_dirs() -> None:
    for path in base.DEFAULT_DIRS:
        if path.exists():
            logging.error(f"Can't create {path} directory. Already exists.")
            sys.exit(1)
        logging.debug(f"Creating dir {path}")
        os.makedirs(path)


def au_init() -> None:
    create_default_dirs()


def check_file(file_path: str) -> str:
    """
    Checks if path exists, is a file, and if absolute if can be made into a au relative path.
    If not raises SystemExit.
    """

    full_path = os.path.join(os.getcwd(), file_path)

    # If file is not in root of the repository then we need to get its full relative path
    if not os.path.exists(os.path.join(cons.REPOSITORY_DIR, file_path)):
        file_path = full_path.split(git.get_git_repo_root())[1]

    if not os.path.exists(full_path):
        logging.error(f"Path '{file_path}' does not exist")
        sys.exit(1)

    if not os.path.isfile(full_path):
        logging.error(f"Path '{file_path}' must be a file")
        sys.exit(1)

    if os.path.isabs(file_path):

        if str(base.cwd) in file_path:
            file_path = file_path.split(str(base.cwd), 1)[1][1:]
        else:
            logging.error(f"File '{file_path}' is not relative to au repository")
            sys.exit(1)

    return file_path
