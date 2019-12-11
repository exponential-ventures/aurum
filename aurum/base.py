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
import argparse
import logging
import os
import shutil
import sys
import json
from pathlib import Path

from aurum import constants as cons
from aurum import git
from aurum.metadata.dataset_meta_data import MetaData, DatasetMetaData, get_dataset_metadata
from aurum.metadata import get_dataset_metadata, DatasetMetaData
from aurum.utils import make_safe_filename

cwd = Path(os.getcwd())

DEFAULT_DIRS = [cwd / cons.REPOSITORY_DIR, cwd / "src", cwd / "logs",
                cwd / os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR)]


def execute_commands(parser: argparse.Namespace):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if parser.verbose else logging.WARNING)

    logging.debug("Parser arguments: {}".format(parser))

    git.check_git()

    if os.getcwd().startswith(os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR)):
        logging.error(f"Cannot run commands from inside '.au' folder")
        sys.exit(1)

    if not hasattr(parser, "subcommand"):
        logging.error(f"No command was passed in")
        sys.exit(1)

    if parser.subcommand == "init":
        run_init(parser)
    elif parser.subcommand == 'data':

        if not git.running_from_git_repo():
            logging.error(f"You are not running from inside a au repository")
            sys.exit(1)

        repo_root = git.get_git_repo_root()

        if not os.path.exists(os.path.join(repo_root, cons.REPOSITORY_DIR)):
            logging.error(f"Path '.au' does not exist, please run au init")
            sys.exit(1)

        if parser.subcommand2 == 'rm':
            run_rm(parser)
        if parser.subcommand2 == 'add':
            run_add(parser)


def run_init(parser: argparse.Namespace):
    logging.info("Initializing git...")
    git.init()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug("Repository {} initialized.".format(cwd))


def run_add(parser: argparse.Namespace):

    if len(parser.files) == 0:
        logging.error(f"Must pass at least one file to be added")
        sys.exit(1)

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


def run_rm(parser):
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


def create_default_dirs():
    for path in DEFAULT_DIRS:
        if path.exists():
            logging.error("Can't create {} directory. Already exists.".format(path))
            sys.exit(1)
        logging.debug(f"Creating dir {path}")
        os.makedirs(path)


def au_init():
    create_default_dirs()

def save_parameters(filename, **kwargs):
    filepath = Path(cons.DATASET_METADATA_DIR, filename)
    mdf = MetaData()
    mdf.paremeters = json.dumps(kwargs)
    meta_data_file_name = mdf.save(filepath)

    git_proc = git.run_git("add", meta_data_file_name)

    result = git_proc.wait()
    if result != 0:
        message = f"Unable to run 'git add {meta_data_file_name} {filename}' Exit code: {result}\n"
        if git_proc.stderr:
            message += f"{git_proc.stderr.read()}\n"
        logging.error(message)

def load_parameters(filename) -> dict:
    filepath = Path(cons.DATASET_METADATA_DIR, filename)
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def check_file(file_path: str) -> str:
    """
    Checks if path exists, is a file, and if absolute if can be made into a au relative path.
    If not raises SystemExit.
    """

    full_path = os.path.join(os.getcwd(), file_path)

    # If file is not in root of the repository then we need to get its full relative path
    if not os.path.exists(os.path.join(cons.REPOSITORY_DIR, file_path)):
        file_path = full_path.split(repo_root)[1]

    if not os.path.exists(full_path):
        logging.error(f"Path '{file_path}' does not exist")
        sys.exit(1)

    if not os.path.isfile(full_path):
        logging.error(f"Path '{file_path}' must be a file")
        sys.exit(1)

    if os.path.isabs(file_path):

        if str(cwd) in file_path:
            file_path = file_path.split(str(cwd), 1)[1][1:]
        else:
            logging.error(f"File '{file_path}' is not relative to au repository")
            sys.exit(1)

    return file_path
