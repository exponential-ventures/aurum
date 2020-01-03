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
from .env_builder import create_temporary_env, install_packages
from .metadata import get_dataset_metadata, DatasetMetaData, MetricsMetaData, ExperimentMetaData, RequirementsMetaData
from .utils import make_safe_filename, is_unnitest_running, dic_to_str


def run_init() -> None:
    logging.info("Initializing git...")
    git.init()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug(f"Repository {base.get_cwd()} initialized.")


def run_add(parsed_result: argparse.Namespace) -> None:
    for f in parsed_result.files:

        full_f = os.path.join(os.getcwd(), f)
        f = check_file(f)

        mdf = DatasetMetaData()
        mdf.file_name = f
        mdf.size = os.path.getsize(full_f)
        meta_data_file_name = mdf.save()

        git_proc = git.run_git("add", full_f, meta_data_file_name, )

        _, err = git_proc.communicate()

        if git_proc.returncode != 0:
            message = f"Unable to run 'git add {meta_data_file_name} {f}' Exit code: {git_proc.returncode}\n"
            if err:
                message += f"{err}\n"

            logging.error(message)
            sys.exit(1)

    sys.stdout.write(f"Added: {parsed_result.files}\n")


def run_rm(parsed_result: argparse.Namespace) -> None:
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


def run_load(parsed_result: argparse.Namespace) -> None:
    logging.info(f"Attempting to load experiment with tag: {parsed_result.tag}")

    experiment_dir = os.path.join(
        git.get_git_repo_root(),
        cons.REPOSITORY_DIR,
        cons.EXPERIMENTS_METADATA_DIR,
    )

    experiments = os.listdir(experiment_dir)
    if f"{parsed_result.tag}.json" not in experiments:
        msg = f"Unknown experiment tag: {parsed_result.tag} "
        logging.debug(msg)
        raise Exception(msg)

    emd = ExperimentMetaData(os.path.join(experiment_dir, f"{parsed_result.tag}.json"))

    requirements_metadata_dir = \
        os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)

    for r in os.listdir(requirements_metadata_dir):
        if r == ".keep":
            continue

        rmd = RequirementsMetaData(os.path.join(requirements_metadata_dir, r))
        if rmd.experiment_id == emd.experiment_id:
            git.run_git("checkout", "-B", f"{parsed_result.tag}")

            virtual_env_dir = create_temporary_env(parsed_result.tag)

            contents = list()

            for line in rmd.contents.splitlines():
                # Skip ourselves
                if "aurum" in line:
                    continue

                contents.append(line)

            install_packages(virtual_env_dir, contents)

            print(f"Please activate your new virtual environment at: {virtual_env_dir}")

            if sys.platform == 'win32':
                bin_name = 'Scripts'
            else:
                bin_name = 'bin'

            full_virtual_env = os.path.join(virtual_env_dir, bin_name, "activate")

            print(f"Run 'source {full_virtual_env}'")

            break


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

    # TODO: Move this code to the test case.
    # This is not a good idea.
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

        if str(base.get_cwd()) in file_path:
            file_path = file_path.split(str(base.get_cwd()), 1)[1][1:]
        else:
            logging.error(f"File '{file_path}' is not relative to au repository")
            sys.exit(1)

    return file_path


def display_metrics(experiment_ids: list) -> None:
    metrics_path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.METRICS_METADATA_DIR)
    for path in os.listdir(metrics_path):
        if cons.KEEP_FILE not in path:
            metrics_metadata = MetricsMetaData(os.path.join(metrics_path, path))
            if len(experiment_ids) > 0:
                if metrics_metadata.experiment_id in experiment_ids:
                    print(dic_to_str(metrics_metadata.metrics, f'Experiment id: {metrics_metadata.experiment_id}'))
            else:
                print(dic_to_str(metrics_metadata.metrics, f'Experiment id: {metrics_metadata.experiment_id}'))
