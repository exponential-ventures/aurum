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


import json
import logging
import os

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from .. import git
from ..utils import gen_file_hash, make_safe_filename


class DatasetMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        super().__init__(file_name)
        self.size = 0

    def save(self, destination: str = None) -> str:
        meta_data_path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR)
        destination = gen_meta_file_name_from_hash(
            meta_data_str=json.dumps(self.serialize()),
            file_name=self.file_name,
            path=meta_data_path,
        )

        self.file_hash = gen_file_hash(os.path.join(git.get_git_repo_root(), self.file_name))

        old_dataset_metadata = DatasetMetaData().get_latest()

        if old_dataset_metadata and self.file_hash != old_dataset_metadata.file_hash:
            self.parent_hash = old_dataset_metadata.file_hash

        logging.debug(f"Saving dataset metadata file to: {destination}")
        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            git.get_git_repo_root(),
            cons.REPOSITORY_DIR,
            cons.DATASET_METADATA_DIR,
        )

    def get_by_ds_name(self, file_name):

        meta_data_dir = os.path.join(self.get_dir(), make_safe_filename(file_name))

        for mdf in os.listdir(meta_data_dir):

            # Ignore keep files.
            if cons.KEEP_FILE in mdf:
                continue

            meta_data_path = os.path.join(meta_data_dir, mdf)
            mdo = DatasetMetaData(meta_data_path)

            if mdo.file_name == file_name:
                return mdo, meta_data_path

        raise FileNotFoundError(f"Metadata not found for {file_name}")
