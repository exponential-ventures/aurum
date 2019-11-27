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

import sys
import os
import logging

from pathlib import Path

from aurum import git


cwd = pathPath(os.getcwd())
dot_au = cwd / ".au"


def execute_commands(parser):
    logging.basicConfig(format="%(levelname)s: %(message)s" ,level=logging.DEBUG if parser.verbose else logging.WARNING)
    
    logging.debug("Parser arguments: {}".format(parser))

    git.check_git()

    if parser.subcommand == 'init':
        run_init(parser)


def run_init(parser):
    logging.info("Initializing git...")
    git.init()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug("Repository {} initialized.".format(current_dir))


def create_dot_au(path):
    if path.exists():
        logging.error("Can't create .au directory. Already exists.")
        sys.exit(1)
    
    os.makedirs(path)

def au_init():
    create_dot_au(dot_au)