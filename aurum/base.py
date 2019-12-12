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
import json
from pathlib import Path

from aurum import constants as cons
from aurum import git
from aurum.commands import run_init, run_rm, run_add
from aurum.metadata import ParameterMetaData

cwd = Path(os.getcwd())

DEFAULT_DIRS = [cwd / cons.REPOSITORY_DIR, cwd / "src", cwd / "logs",
                cwd / os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR),
                cwd / os.path.join(cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR)]


def execute_commands(parser: argparse.ArgumentParser) -> None:
    parsed = parser.parse_args()

    logging.basicConfig(format="%(levelname)s: %(message)s",
                        level=logging.DEBUG if parsed.verbose else logging.WARNING)

    logging.debug(f"Parser arguments: {parsed}")

    git.check_git()

    if os.getcwd().startswith(os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR)):
        parser.error(f"Cannot run commands from inside '.au' folder")

    if not hasattr(parsed, "subcommand"):
        parser.error(f"No command was passed in")

    if parsed.subcommand == "init":
        run_init(parsed)
    elif parsed.subcommand == "data":

        if hasattr(parsed, "subcommand2") and parsed.subcommand2 == "rm":
            data_command_checker(parser)
            run_rm(parsed)
        if hasattr(parsed, "subcommand2") and parsed.subcommand2 == "add":
            data_command_checker(parser)
            run_add(parsed)
        else:
            parser.error("Unknown command for data")


def data_command_checker(parser: argparse.ArgumentParser):
    if not git.running_from_git_repo():
        parser.error(f"You are not running from inside a au repository")

    repo_root = git.get_git_repo_root()

    if not os.path.exists(os.path.join(repo_root, cons.REPOSITORY_DIR)):
        parser.error(f"Path '.au' does not exist, please run au init")


def parameters(**kwargs):
    from aurum.commands import parser as p

    for param, default in kwargs.items():
        if param not in p.known_params:
            p.parser.add_argument(f'-{param}', required=False, default=default)

    p.parse_args()

    if len(p.unknown_params) > 0:
        logging.warning(f"Unknown parameters passed to experiment are being ignored: {' '.join(p.unknown_params)}")

    new_dict = {**kwargs, **p.known_params.__dict__}

    for key in new_dict.keys():
        setattr(sys.modules['aurum'], key, new_dict[key])

    save_parameters(**new_dict)


def save_parameters(**kwargs):
    mdf = ParameterMetaData()
    mdf.parameters = json.dumps(kwargs)
    meta_data_file_name = mdf.save()

    if meta_data_file_name:

        git_proc = git.run_git("add", meta_data_file_name)

        result = git_proc.wait()
        if result != 0:
            message = f"Unable to run 'git add {meta_data_file_name}' Exit code: {result}\n"
            if git_proc.stderr:
                message += f"{git_proc.stderr.read()}\n"
            logging.error(message)


def save_metrics():
    pass
