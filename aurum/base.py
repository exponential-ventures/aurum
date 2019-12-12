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
from pathlib import Path

from aurum import constants as cons
from aurum import git
from aurum.commands import run_init, run_rm, run_add

cwd = Path(os.getcwd())

DEFAULT_DIRS = [cwd / cons.REPOSITORY_DIR, cwd / "src", cwd / "logs",
                cwd / os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR)]


def execute_commands(parser: argparse.ArgumentParser) -> None:
    parsed = parser.parse_args()

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if parsed.verbose else logging.WARNING)

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
