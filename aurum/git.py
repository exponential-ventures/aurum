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

import logging
import sys
from subprocess import Popen, PIPE


def check_git():
    process = run_git('--version')
    output = process.communicate()[0].decode('utf-8')

    if "git version" in output:
        logging.debug("Git found.")
        return

    logging.error("Git not installed. Aborting.")
    sys.exit(1)


def init():
    run_git('init')

def rm(filepath, soft_delete : bool = True):
    # TODO: remove the file from metadata
    if soft_delete:
        run_git('rm','--cached', filepath)
    else:
        run_git('rm', filepath)


def run_git(*args):
    logging.debug(f"Running git {args}")
    return Popen(['git'] + list(args), stdout=PIPE)
