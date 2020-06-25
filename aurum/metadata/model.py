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

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons, git
from ..theorem import Theorem
from ..utils import gen_dict_hash

class ModelMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.model = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        mmd = ModelMetaData()

        parent = mmd.get_latest()
        self.file_hash = gen_dict_hash(self.model)

        if parent and self.file_hash != parent.file_hash and Theorem().has_any_change():
            self.parent_hash = parent.file_hash

        destination = gen_meta_file_name_from_hash(str(self.timestamp), '', mmd.get_dir())
        logging.debug(f"Saving model file to: {destination}")
        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            git.get_git_repo_root(),
            cons.REPOSITORY_DIR,
            cons.MODELS_METADATA_DIR,
        )