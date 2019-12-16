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

import hashlib
import os
import json
import ntpath
from datetime import datetime

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.utils import make_safe_filename


class ParameterMetaData(MetaData):
    """
    Responsible for interacting with Meta Data files:
    - Accessing attributes such as hashes and timestamps ect.
    - Serialize and deserialize from file format.
    - Generate file hash.
    - Generate meta data hash.
    - Generate meta data file name.
    - TODO: Traverse a dataset's history.
    """

    def __init__(self, file_name: str = '') -> None:
        self.parent_file_name = None
        self.timestamp = datetime.now()

        if file_name != '':
            with open(file_name, 'r') as f:
                self.deserialize(f.read())

    def deserialize(self, raw_json: str):
        super().deserialize(raw_json)
        self.timestamp = datetime.fromtimestamp(self.timestamp)

    def save(self, destination: str = None) -> str:
        create_file = True

        old_parameters = load_parameters()
        if old_parameters:
            new_parameters = json.loads(self.parameters)
            create_file = should_create_new_file(old_parameters, new_parameters)
            metadata = get_parameter_metadata()
            self.parent_file_name = ntpath.basename(metadata[0])

        if create_file:
            if destination is None:
                destination = gen_meta_file_name(str(self.timestamp), '')
            return super().save(destination)

        return None


def get_parameter_metadata() -> (str, ParameterMetaData):
    meta_data_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR)

    if os.path.exists(meta_data_dir):
        for mdf in os.listdir(meta_data_dir):
            mdf_path = os.path.join(meta_data_dir, mdf)

            mdo = ParameterMetaData(mdf_path)
            return mdf_path, mdo

    return None, None


def gen_meta_hash(meta_data_str):
    meta_data_file_name = hashlib.sha1()
    meta_data_file_name.update(str.encode(meta_data_str))
    return meta_data_file_name.hexdigest()


def gen_meta_file_name(meta_data_str, file_name):
    path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR)

    meta_data_dir = os.path.join(path, make_safe_filename(file_name))

    if not os.path.exists(meta_data_dir):
        os.mkdir(meta_data_dir)

    meta_hash = gen_meta_hash(meta_data_str)
    meta_data_file_name = meta_hash + ".json"

    return os.path.join(meta_data_dir, meta_data_file_name)


def load_parameters() -> dict:
    metadata = get_parameter_metadata()
    filepath = metadata[0]
    if filepath:
        with open(filepath, 'r') as f:
            root_json = json.loads(f.read())
            return json.loads(root_json['parameters'])
    else:
        return {}


def should_create_new_file(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    if (len(same) == len(d1)):
        return False

    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys

    if (len(added) > 0) or (len(removed) > 0):
        return True

    for k in intersect_keys:
        if d1[k] != d2[k]:
            return True

    return False
