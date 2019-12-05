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
import sys
from datetime import datetime
from pathlib import Path

from aurum import git
from aurum.meta_data import MetaData, get_metadata

cwd = Path(os.getcwd())

DEFAULT_DIRS = [cwd / ".au", cwd / "src", cwd / "logs"]


def execute_commands(parser: argparse.Namespace):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if parser.verbose else logging.WARNING)

    logging.debug("Parser arguments: {}".format(parser))

    git.check_git()

    if not hasattr(parser, "subcommand"):
        sys.stderr.write(f"No command was passed in \n")
        sys.exit(1)

    if parser.subcommand == "init":
        run_init(parser)
    elif parser.subcommand == 'data':
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
    logging.debug(f"Adding files to aurum: {parser.files}")

    if not os.path.exists('.au'):
        sys.stderr.write(f"Path '.au' does not exist, please run au init \n")
        sys.exit(1)

    for file in parser.files:
        if not os.path.exists(file):
            sys.stderr.write(f"Path '{file}' does not exist! \n")
            sys.exit(1)

        if not os.path.isfile(file):
            sys.stderr.write(f"Path '{file}' must be a file! \n")
            sys.exit(1)

        mdf = MetaData()
        mdf.file_name = file
        mdf.timestamp = datetime.now()
        mdf.size = os.path.getsize(file)
        mdf.parent_hash = None
        mdf.gen_file_hash()
        meta_data_file_name = mdf.deserialize()

        git_proc = git.run_git(
            "add",
            f"{meta_data_file_name}",
            f"{file}",
        )

        result = git_proc.wait()

        if result != 0:
            sys.stderr.write(f"Unable to run 'git add {meta_data_file_name} {file}' {git_proc.stderr.read()}\n")
            sys.exit(1)


def run_rm(parser):
    for filepath in parser.files:
        logging.info(f"Removing {filepath} from git")
        git.rm(filepath, soft_delete=parser.soft_delete)
        logging.info(f"{filepath} removed from git")

        meta_data_path, _ = get_metadata(filepath)

        if meta_data_path:

            logging.info(f"Removing meta data '{meta_data_path}' and removing from git.")

            git.rm(meta_data_path, soft_delete=parser.soft_delete)

            # might have been removed by git, might not.
            if os.path.exists(meta_data_path):
                os.remove(meta_data_path)

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
