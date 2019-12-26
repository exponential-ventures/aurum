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
import logging

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.metadata.metadata import gen_meta_file_name_from_hash
from aurum.utils import gen_dict_hash, dir_files_by_last_modification_date

META_DATA_DIR = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.METRICS_METADATA_DIR)


class MetricsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.metrics = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        parent_metrics_metadata = get_latest_metrics_metadata()
        self.file_hash = gen_dict_hash(self.metrics)

        if self.file_hash != parent_metrics_metadata.file_hash:
            self.parent_hash = parent_metrics_metadata.file_hash
            destination = gen_meta_file_name_from_hash(str(self.timestamp), '', META_DATA_DIR)
            logging.debug(f"Saving metric file to: {destination}")

            return super().save(destination)


def get_latest_metrics_metadata() -> MetricsMetaData:
    files = dir_files_by_last_modification_date(META_DATA_DIR)

    if len(files) > 0:
        return MetricsMetaData(files[0][1])

    return MetricsMetaData()
