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
from .. import constants as cons, git


class RequirementsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.contents = None
        super().__init__(file_name)

    def save(self, cwd: str, destination: str = None) -> str:
        name = f"{self.file_hash}.json"

        destination = os.path.join(self.get_dir(), name)

        return super().save(destination=destination, cwd=cwd)

    def get_dir(self):
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.REQUIREMENTS_METADATA_DIR,
        )
