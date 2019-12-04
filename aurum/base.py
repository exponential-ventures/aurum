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
from pathlib import Path

from aurum import git

cwd = Path(os.getcwd())

DEFAULT_DIRS = [cwd / ".au.py", cwd / "src", cwd / "logs"]


def execute_commands(parser: argparse.Namespace):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if parser.verbose else logging.WARNING)

    logging.debug("Parser arguments: {}".format(parser))

    git.check_git()

    if parser.subcommand == "init":
        run_init(parser)
    elif parser.subcommand == "add":
        run_add(parser)


def run_init(parser: argparse.Namespace):
    logging.info("Initializing git...")
    git.init()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug("Repository {} initialized.".format(cwd))


def run_add(parser: argparse.Namespace):
    logging.debug(f"Adding files to aurum: {parser.files}")


def create_default_dirs():
    for path in DEFAULT_DIRS:
        if path.exists():
            logging.error("Can't create {} directory. Already exists.".format(path))
            sys.exit(1)

        os.makedirs(path)


def au_init():
    create_default_dirs()
