#!/usr/bin/env python3
##
## Authors: Rhuan Karlus
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
import time

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from ..theorem import Theorem
from ..utils import gen_dict_hash


class WeightsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.weights = None
        self.binary_file_path = ''
        super().__init__(file_name)

    def save(self, cwd: str, destination: str = None) -> str:
        current_timestamp = str(round(time.time() * 1000))

        if Theorem().has_any_change():
            self.file_hash = gen_dict_hash({
                'binary_file_path': self.binary_file_path,
            })
            parent = self.get_latest(subdir_path=os.path.join(cwd, cons.REPOSITORY_DIR, cons.WEIGHTS_METADATA_DIR))
            if parent and self.file_hash != parent.file_hash:
                self.parent_hash = parent.file_hash

        if destination is None:
            destination = gen_meta_file_name_from_hash(str(current_timestamp), '', self.get_dir())

        logging.debug(f"Saving model file to: {destination}")
        return super().save(destination=destination, cwd=cwd)

    def save_binary(self, encoded_model: bytes, cwd: str = '', destination: str = None) -> str:

        current_timestamp = str(round(time.time() * 1000))

        if cwd == '':
            cwd = os.getcwd()

        if destination is None:
            binary_file_path = os.path.join(cwd, self.get_binaries_dir(), current_timestamp)
        else:
            binary_file_path = destination

        with open(binary_file_path, 'wb') as f:
            f.write(encoded_model)

        self.binary_file_path = binary_file_path

        return self.binary_file_path

    def get_dir(self):
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.WEIGHTS_METADATA_DIR,
        )

    @staticmethod
    def load_binary(destination: str):
        with open(destination, mode='rb') as f:
            return f.read()

    @staticmethod
    def get_binaries_dir():
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.WEIGHTS_METADATA_DIR,
            cons.WEIGHTS_BINARIES_DIR,
        )
