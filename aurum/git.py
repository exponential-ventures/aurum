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
import os
import subprocess
import sys


def check_git():
    process = run_git("--version")
    output = process.communicate()[0].decode("utf-8")

    if "git version" not in output:
        logging.error("Git not installed. Aborting.")
        sys.exit(1)

    logging.debug("Git found.")


def running_from_git_repo() -> bool:
    process = subprocess.Popen(
        ["git", "rev-parse", "--is-inside-work-tree"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=os.getcwd(),
    )
    output, _ = process.communicate()
    output = output.decode("utf-8")

    return str(output) == "true\n"


def get_git_repo_root() -> str:

    if not running_from_git_repo():
        logging.warning("Not running from a git repo")
        return ""

    process = run_git(
        "rev-parse",
        "--show-toplevel"
    )

    output, _ = process.communicate()
    return output.decode("utf-8").replace("\n", "/")


def init():
    run_git("init").wait()


def rm(filepath, soft_delete: bool = True):
    if soft_delete:
        run_git("rm", "--cached", filepath).wait()
    else:
        run_git("rm", filepath).wait()


def run_git(*args):
    return subprocess.Popen(["git"] + list(args), stdout=subprocess.PIPE)
