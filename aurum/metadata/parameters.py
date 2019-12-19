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

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.metadata.metadata import gen_meta_file_name_from_hash


class ParameterMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        super().__init__(file_name)
        self.parameters = None

    def save(self, destination: str = None) -> str:
        parent_parameter_metadata = get_latest_parameter()

        if parent_parameter_metadata.timestamp < self.timestamp:
            self.parent_hash = parent_parameter_metadata.file_hash

        destination_path = os.path.join(git.get_git_repo_root(),
                                        cons.REPOSITORY_DIR,
                                        cons.PARAMETER_METADATA_DIR)
        destination = gen_meta_file_name_from_hash(
            meta_data_str=str(self.timestamp),
            file_name='',
            path=destination_path
        )
        return super().save(destination)


def get_latest_parameter() -> ParameterMetaData:
    newest = ParameterMetaData()

    parameter_metadata_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR)

    for file in os.listdir(parameter_metadata_dir):

        full_path = os.path.join(parameter_metadata_dir, file)

        pmd = ParameterMetaData(full_path)

        if pmd.timestamp < newest.timestamp:
            newest = pmd

    return newest
