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


import hashlib
import logging
import os
import subprocess
from . import constants as cons

from .metadata import RequirementsMetaData


def is_new_requirements(cwd: str = '') -> (bool, str):
    """
    Run a pip freeze and create a hash to be saved in the requirements metadata, remember that we will also need to
    record the parent requirements (latest by date, if it exists) as well as all the contents of the pip freeze list
    in a alphabetically sorted list.

    Make sure that the metadata is a linked list and can be easily browsed to find the parent even if you don't know
    who the parent is (similar to all other metadata implemented in the system).

    If there is a change in the results from freeze, this module should indicate that this is a new experiment, and
    create the metadata to document this. If there is no previous metadata (experiment is being run for the first time)
    then the code should proceed as if this is a brand new experiment, except that parent will be None.
    """

    if cwd == '':
        cwd = os.getcwd()

    process = subprocess.run(
        "pip freeze",
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
    )
    output = process.stdout
    logging.debug(f"\nInstalled packages: \n {output} \n\n")
    packages_hash = hashlib.sha1()
    packages_hash.update(output)
    packages_hash = packages_hash.hexdigest()

    latest_mdf = RequirementsMetaData().get_latest(
        subdir_path=os.path.join(cwd, cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)
    )

    if not latest_mdf:
        logging.debug("This is a new requirements")
        rmd = RequirementsMetaData()
        rmd.file_hash = packages_hash
        rmd.contents = output.decode()
        rmd.save(cwd=cwd)
        return True, rmd.file_hash

    elif latest_mdf and latest_mdf.file_hash != packages_hash:
        logging.debug("This are changed requirements")
        rmd = RequirementsMetaData()
        rmd.file_hash = packages_hash
        rmd.parent_hash = latest_mdf.file_hash
        rmd.contents = output.decode()
        rmd.save(cwd=cwd)
        return True, rmd.file_hash

    return False, ""
