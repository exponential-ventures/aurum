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
import subprocess

from aurum import git


def run_test_init():
    proc = subprocess.Popen(
        ["au -v init"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    _, e = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"Unable to run init. {e} {proc.returncode}")


def set_git_for_test():
    proc = git.run_git('config', '--global', 'user.email', '"test@example.com"', )
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    proc = git.run_git('config', '--global', 'user.name', '"test"', )
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    logging.debug("Git config successful")
