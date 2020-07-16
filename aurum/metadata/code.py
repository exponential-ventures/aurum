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
from glob import glob

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons, git
from ..utils import gen_file_hash


class CodeMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.file_path_and_hash = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        destination_path = os.path.join(cons.REPOSITORY_DIR, cons.CODE_METADATA_DIR)
        destination = gen_meta_file_name_from_hash(
            meta_data_str=str(self.timestamp),
            file_name='',
            path=destination_path
        )
        self.file_hash = self.file_path_and_hash
        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.CODE_METADATA_DIR,
        )


def list_src_files() -> list:
    path = cons.SOURCE_CODE_DIR
    return glob(f"{path}/*")


def generate_src_files_hash_dict() -> dict:
    new_dict = {}
    for p in list_src_files():
        new_dict[p] = gen_file_hash(p)

    return new_dict


def generate_src_files_hash() -> str:
    main_hash = hashlib.sha1()

    for p in list_src_files():
        if os.path.isdir(p):
            continue
        main_hash.update(gen_file_hash(p).encode())

    return main_hash.hexdigest()
