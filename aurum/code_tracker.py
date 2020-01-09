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

from .metadata import CodeMetaData, generate_src_files_hash


def is_new_code() -> (bool, str):
    # Generate the current code hash string
    current_code_hash = generate_src_files_hash()

    # Get the latest saved version of the code
    latest = CodeMetaData().get_latest()

    def save_code_metadata(parent_hash: str = None) -> None:
        cmd = CodeMetaData()
        cmd.file_path_and_hash = current_code_hash
        cmd.parent_hash = parent_hash
        if parent_hash:
            logging.debug(f"Saving CodeMetaData latest file_path_and_hash: {latest.file_path_and_hash} "
                          f"and with file_path_and_hash: {current_code_hash} ")
        else:
            logging.debug(f"Saving CodeMetaData without latest and with file_path_and_hash: {current_code_hash} ")
        cmd.save()

    # If we don't have a latest. then this is the first run.
    if not latest:
        save_code_metadata()
        return True, current_code_hash

    # If we do have a latest and the file hash has changed.
    if latest and latest.file_path_and_hash != current_code_hash:
        save_code_metadata(latest.file_path_and_hash)
        return True, current_code_hash

    # Code has not changed and is the same as it was in latest
    return False, latest.file_path_and_hash
