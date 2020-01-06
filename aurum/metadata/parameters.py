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

from aurum import git
from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from ..utils import gen_dict_hash, dir_files_by_last_modification_date


class ParameterMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.parameters = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        parent_parameter_metadata = get_latest_parameter()
        self.file_hash = gen_dict_hash(self.parameters)

        if self.file_hash != parent_parameter_metadata.file_hash:
            self.parent_hash = parent_parameter_metadata.file_hash

            parameter_metadata_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR,
                                                  cons.PARAMETER_METADATA_DIR)

            destination = gen_meta_file_name_from_hash(
                meta_data_str=str(self.timestamp),
                file_name='',
                path=parameter_metadata_dir
            )
            logging.debug(f"Saving parameters file to: {destination}")
            return super().save(destination)

    @property
    def parameter_hash(self) -> str:
        return gen_dict_hash(self.parameters)


def get_latest_parameter() -> ParameterMetaData:
    parameter_metadata_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR,
                                          cons.PARAMETER_METADATA_DIR)

    files = dir_files_by_last_modification_date(parameter_metadata_dir)

    if len(files) > 0:
        return ParameterMetaData(files[0][1])

    return ParameterMetaData()
