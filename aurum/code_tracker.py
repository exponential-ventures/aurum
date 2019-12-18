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

import ntpath

from aurum.metadata import CodeMetaData, load_code, generate_src_files_hash, get_code_metadata
from aurum.utils import should_create_new_file


def is_new_code() -> bool:
    mdt = CodeMetaData()
    old_code_references = load_code()
    new_code_references = generate_src_files_hash()

    is_new = should_create_new_file(new_code_references, old_code_references)

    if is_new:
        metadata = get_code_metadata()
        mdt.file_path_and_hash = new_code_references
        if metadata[0]:
            mdt.parent_file_name = ntpath.basename(metadata[0])
        mdt.save()

    return is_new
