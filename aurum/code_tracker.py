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

from aurum.metadata import CodeMetaData, generate_src_files_hash, get_code_metadata
from aurum.utils import gen_dict_hash


def is_new_code() -> bool:
    mdt = CodeMetaData()
    old_code_references = get_code_metadata()
    new_code_references = generate_src_files_hash()

    if len(new_code_references) == 0:
        return False

    mdt.file_hash = gen_dict_hash(new_code_references)

    is_new = mdt.file_hash != old_code_references.file_hash

    if is_new:
        mdt.file_path_and_hash = new_code_references
        mdt.parent_hash = old_code_references.file_hash
        mdt.save()

    return is_new
