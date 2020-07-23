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

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from ..theorem import Theorem
from ..utils import gen_dict_hash


class MetricsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.metrics = None
        super().__init__(file_name)

    def save(self, cwd: str, destination: str = None) -> str:

        mmd = MetricsMetaData()
        parent = mmd.get_latest(subdir_path=os.path.join(cwd, cons.REPOSITORY_DIR, cons.METRICS_METADATA_DIR))

        self.file_hash = gen_dict_hash(self.metrics)

        if parent and self.file_hash != parent.file_hash and Theorem().has_any_change():
            self.parent_hash = parent.file_hash

        destination = gen_meta_file_name_from_hash(
            meta_data_str=str(self.timestamp),
            file_name='',
            path=os.path.join(cons.REPOSITORY_DIR, cons.METRICS_METADATA_DIR)
        )

        return super().save(cwd=cwd, destination=destination)

    def get_dir(self):
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.METRICS_METADATA_DIR,
        )
