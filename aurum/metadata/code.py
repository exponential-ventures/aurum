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
import os
from datetime import datetime
from glob import glob

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from .. import git
from ..utils import gen_file_hash, dir_files_by_last_modification_date

CODE_METADATA_PATH = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.CODE_METADATA_DIR)


class CodeMetaData(MetaData):
    """
    Responsible for interacting with Meta Data files:
    - Accessing attributes such as hashes and timestamps ect.
    - Serialize and deserialize from file format.
    - Generate file hash.
    - Generate meta data hash.
    - Generate meta data file name.
    - TODO: Traverse a code's history.
    """

    def __init__(self, file_name: str = '') -> None:
        super().__init__(file_name)
        self.file_path_and_hash = None

    def save(self, destination: str = None) -> str:
        destination_path = os.path.join(git.get_git_repo_root(),
                                        cons.REPOSITORY_DIR,
                                        cons.CODE_METADATA_DIR)
        destination = gen_meta_file_name_from_hash(
            meta_data_str=str(self.timestamp),
            file_name='',
            path=destination_path
        )
        return super().save(destination)


def get_code_metadata() -> CodeMetaData:
    file_last_modified_list = dir_files_by_last_modification_date(CODE_METADATA_PATH)

    if len(file_last_modified_list) > 0:
        return CodeMetaData(file_last_modified_list[0][1])

    return CodeMetaData()


def list_src_files() -> list:
    path = os.path.join(git.get_git_repo_root(), cons.SOURCE_CODE_DIR)
    return glob(f"{path}/*")


def generate_src_files_hash_dict() -> dict:
    new_dict = {}
    for p in list_src_files():
        new_dict[p] = gen_file_hash(p)

    return new_dict


def generate_src_files_hash() -> str:
    main_hash = hashlib.sha1()

    for p in list_src_files():
        main_hash.update(gen_file_hash(p))

    return main_hash.hexdigest()


def get_latest_code_metadata_by_date() -> CodeMetaData:
    newest = None
    now = datetime.now()

    code_metadata_dir = os.path.join(
        git.get_git_repo_root(),
        cons.REPOSITORY_DIR,
        cons.CODE_METADATA_DIR,
    )

    for file in os.listdir(code_metadata_dir):

        full_path = os.path.join(code_metadata_dir, file)

        cmd = CodeMetaData(full_path)
        if now > cmd.timestamp:
            newest = cmd
            now = cmd.timestamp

    return newest
