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


import os

from .metadata import MetaData
from .. import constants as cons
from .. import git
from ..utils import gen_dict_hash


class ExperimentMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.name = None
        self.dataset_hash = None
        self.code_hash = None
        self.parameter_hash = None
        self.requirements_hash = None
        self.logging_hash = None
        self.weights_hash = None
        super().__init__(file_name)

    def save(self, destination: str) -> str:
        self.file_hash = self.obj_hash()

        parent = self.get_latest()

        if parent and parent.file_hash != self.file_hash:
            self.parent_hash = parent.file_hash

        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.EXPERIMENTS_METADATA_DIR,
        )

    def obj_hash(self):
        return gen_dict_hash(
            {
                'code_hash': self.code_hash,
                'dataset_hash': self.dataset_hash,
                'parameter_hash': self.parameter_hash,
                'parent_hash': self.parent_hash,
                'requirements_hash': self.requirements_hash,
            }
        )
