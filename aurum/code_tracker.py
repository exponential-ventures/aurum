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

from .metadata import CodeMetaData
from .metadata.code import get_latest_code_metadata_by_date, generate_src_files_hash


def is_new_code() -> (bool, str):

    # Generate the current code hash string
    current_code_hash = generate_src_files_hash()

    # Get the latest saved version of the code
    latest = get_latest_code_metadata_by_date()

    cmd = CodeMetaData()

    # If not latest, then this is the first run so the current code is new or the hash is different.
    if not latest or latest.file_path_and_hash != current_code_hash:

        cmd.file_path_and_hash = current_code_hash

        if latest:
            cmd.parent_hash = latest.file_path_and_hash

        cmd.save()

        return True, current_code_hash

    # Code has not changed and is the same as it was in latest
    return False, latest.file_path_and_hash
