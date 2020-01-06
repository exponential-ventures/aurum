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
        logging.debug("Not running from a git repo")
        return ""

    process = run_git(
        "rev-parse",
        "--show-toplevel"
    )

    output, _ = process.communicate()
    return output.decode("utf-8").replace("\n", "/")


def init():
    p = run_git("init")
    _, err = p.communicate()
    if p.returncode != 0:
        raise Exception(f"Failed to run 'git init': {err}")


def rm(filepath, soft_delete: bool = True):
    if soft_delete:
        run_git("rm", "--cached", filepath).wait()
    else:
        run_git("rm", filepath).wait()


def add_dirs(dirs: list) -> None:
    for path in dirs:
        process = run_git('add', path)
        _, error = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Failed to run 'git add {path}': {error}")


def tag(experiment_id: str, message: str) -> None:
    process = run_git('tag', '-a', experiment_id, '-m', message)
    _, error = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Failed to run 'git tag -a {experiment_id} -m {message}': {error}")


def commit(commit_message: str, secondary_msg: str = '') -> None:
    if secondary_msg is not '':
        process = run_git('commit', '-am', commit_message, '-m', secondary_msg)
    else:
        process = run_git('commit', '-am', commit_message)

    _, error = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Failed to run 'git commit -am {commit_message} -m {secondary_msg}': {error}")


def last_commit_hash() -> str:
    process = run_git('rev-parse', 'HEAD')

    output, error = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Failed to run 'git rev-parse': {error}")

    return output.decode('utf-8').replace('\n', '')


def current_branch_name() -> str:
    process = run_git('rev-parse', '--abbrev-ref', 'HEAD')
    output, error = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Failed to run 'git rev-parse --abbrev-ref HEAD': {error}")

    return output.decode('utf-8').replace('\n', '')


def run_git(*args):
    return subprocess.Popen(["git"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
