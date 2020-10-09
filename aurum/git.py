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


class GitCommandError(Exception):
    pass


def check_git():
    process = run_git("--version")
    output = process.communicate()[0].decode("utf-8")

    if "git version" not in output:
        logging.error("Git not installed. Aborting.")
        sys.exit(1)

    logging.debug("Git found.")


def running_from_git_repo(cwd: str = "") -> bool:
    if cwd == "":
        cwd = os.getcwd()

    process = subprocess.Popen(
        ["git", "rev-parse", "--is-inside-work-tree"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=cwd,
    )
    output, _ = process.communicate()
    output = output.decode("utf-8")

    return str(output) == "true\n"


def get_git_repo_root(cwd: str = '') -> str:
    if cwd == "":
        cwd = os.getcwd()

    if not running_from_git_repo(cwd):
        logging.debug("Not running from a git repo")
        return ""

    process = run_git(
        "rev-parse",
        "--show-toplevel",
        cwd=cwd
    )

    output, _ = process.communicate()
    return output.decode("utf-8").replace("\n", "/")


def init():
    p = run_git("init")
    _, err = p.communicate()
    if p.returncode != 0:
        raise GitCommandError(f"Failed to run 'git init': {err}")


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
            raise GitCommandError(f"Failed to run 'git add {path}': {error}")


def tag(experiment_id: str, message: str) -> None:
    process = run_git('tag', '-a', experiment_id, '-m', message)
    _, error = process.communicate()

    if process.returncode != 0:
        raise GitCommandError(f"Failed to run 'git tag -a {experiment_id} -m {message}': {error}")


def commit(commit_message: str, secondary_msg: str = '', cwd: str = '') -> (str, str):
    if secondary_msg is not '':
        process = run_git('commit', '-am', commit_message, '-m', secondary_msg, cwd=cwd)
    else:
        process = run_git('commit', '-am', commit_message, cwd=cwd)

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise GitCommandError(
            f"Failed to run 'git commit -am {commit_message} -m {secondary_msg}': {stdout} -- {stderr}")

    return stdout, stderr


def last_commit_hash() -> str:
    process = run_git('rev-parse', 'HEAD')

    output, error = process.communicate()

    if process.returncode != 0:
        raise GitCommandError(f"Failed to run 'git rev-parse': {error}")

    return output.decode('utf-8').replace('\n', '')


def current_branch_name() -> str:
    process = run_git('rev-parse', '--abbrev-ref', 'HEAD')
    output, error = process.communicate()

    if process.returncode != 0:
        raise GitCommandError(f"Failed to run 'git rev-parse --abbrev-ref HEAD': {error}")

    return output.decode('utf-8').replace('\n', '')


def push() -> str:
    if not has_remote():
        return ''
    sub = run_git('push', '--all')
    output, error = sub.communicate()
    if sub.returncode != 0:
        raise GitCommandError(f"Failed to run 'git push --all': {error}")

    return output.decode('utf-8').replace('\n', '')


def push_tags() -> str:
    if not has_remote():
        return ''
    sub = run_git('push', '--tags')
    output, error = sub.communicate()
    if sub.returncode != 0:
        raise GitCommandError(f"Failed to run 'git push --tags': {error}")
    return output.decode('utf-8').replace('\n', '')


def has_remote() -> bool:
    sub = run_git('remote', 'show')
    output, error = sub.communicate()
    if sub.returncode != 0:
        raise GitCommandError(f"Failed to run 'git remote show': {error} /n Please configure a remote repository")

    output = output.decode('utf-8').replace('\n', '')
    return bool(output and output.strip())


def add(*filenames: str, cwd: str = '') -> str:
    sub = run_git('add', *filenames, cwd=cwd)
    stdout, stderr = sub.communicate()

    if sub.returncode != 0:
        raise GitCommandError(f"Failed to run 'git add {filenames}': {stderr}")

    return stdout.decode('utf-8').replace('\n', '')


def run_git(*args, cwd: str = ''):
    if cwd == '':
        cwd = os.getcwd()
    return subprocess.Popen(["git"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
