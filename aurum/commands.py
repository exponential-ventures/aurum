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
from pathlib import Path

from . import constants as cons, base, git
from .metadata import get_dataset_metadata, DatasetMetaData
from .utils import make_safe_filename, is_unnitest_running


def run_init() -> None:
    logging.info("Initializing git...")
    git.init()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug(f"Repository {base.cwd} initialized.")


def run_add(parsed_result: argparse.Namespace) -> None:
    for f in parsed_result.files:

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

    sys.stdout.write(f"Added: {parsed_result.files}\n")


def run_rm(parsed_result) -> None:
    for filepath in parsed_result.files:

        filepath = check_file(filepath)

        logging.info(f"Removing {filepath} from git")
        git.rm(filepath, soft_delete=parsed_result.soft_delete)
        logging.info(f"{filepath} removed from git")

        meta_data_path, _ = get_dataset_metadata(filepath)

        if meta_data_path:

            logging.info(f"Removing meta data '{meta_data_path}' and removing from git.")

            git.rm(meta_data_path, soft_delete=parsed_result.soft_delete)

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
        Path(path, '.keep').touch()  # Needed to allow adding an empty directory to git


def au_init() -> None:
    create_default_dirs()
    git.add_dirs(base.DEFAULT_DIRS)
    logging.info("Adding directories to git...")

    if not is_unnitest_running():
        git.commit('Initial Commit')
        logging.info("Initial commit")


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
