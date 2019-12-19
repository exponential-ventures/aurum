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
import json
from glob import glob
from datetime import datetime

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData, gen_meta_file_name_from_hash
from aurum.utils import gen_file_hash

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
        self.file_path_and_hash = None
        self.parent_file_name = None
        self.timestamp = datetime.now()

        if file_name != '':
            with open(file_name, 'r') as f:
                self.deserialize(f.read())

    def deserialize(self, raw_json: str):
        super().deserialize(raw_json)
        self.timestamp = datetime.fromtimestamp(self.timestamp)

    def save(self, destination: str = None) -> str:
        if destination is None:
            destination_path = os.path.join(git.get_git_repo_root(),
                                            cons.REPOSITORY_DIR,
                                            cons.CODE_METADATA_DIR)
            destination = gen_meta_file_name_from_hash(
                meta_data_str=str(self.timestamp),
                file_name='',
                path=destination_path
            )
        return super().save(destination)


def get_code_metadata() -> (str, CodeMetaData):
    if os.path.exists(CODE_METADATA_PATH):
        for mdf in os.listdir(CODE_METADATA_PATH):
            mdf_path = os.path.join(CODE_METADATA_PATH, mdf)

            mdo = CodeMetaData(mdf_path)
            return mdf_path, mdo

    return None, None


def load_code() -> dict:
    metadata = get_code_metadata()
    filepath = metadata[0]
    if filepath:
        with open(filepath, 'r') as f:
            root_json = json.loads(f.read())
            return json.loads(root_json['file_path_and_hash'])
    else:
        return {}


def list_src_files() -> list:
    path = os.path.join(git.get_git_repo_root(), cons.SOURCE_CODE_DIR)
    return glob(f"{path}/*")


def generate_src_files_hash() -> dict:
    new_dict = {}
    for p in list_src_files():
        new_dict[p] = gen_file_hash(p)

    return new_dict
