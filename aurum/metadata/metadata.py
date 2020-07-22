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


"""
MetaData objects allow a user to:
  - dynamically add instance attributes and have them be json serializable.
  - serialize: convert json string naive(str only) MetaData object.
  - deserialize: convert MetaData object to json string.
  - save: perform a deserialization and save to file.
"""
import hashlib
import json
import logging
import os
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Collection, Mapping, Union
from uuid import UUID

from .. import constants as cons
from ..dry_run import dehydratable
from ..theorem import Theorem
from ..utils import make_safe_filename


def _isinstance_safe(o, t):
    try:
        result = isinstance(o, t)
    except Exception:
        return False
    else:
        return result


Json = Union[dict, list, str, int, float, bool, None]


class _ExtendedEncoder(json.JSONEncoder):
    def default(self, o) -> Json:
        result: Json
        if _isinstance_safe(o, Collection):
            if _isinstance_safe(o, Mapping):
                result = dict(o)
            else:
                result = list(o)
        elif _isinstance_safe(o, datetime):
            result = o.timestamp()
        elif _isinstance_safe(o, UUID):
            result = str(o)
        elif _isinstance_safe(o, Enum):
            result = o.value
        elif _isinstance_safe(o, Decimal):
            result = str(o)
        else:
            result = json.JSONEncoder.default(self, o)
        return result


class MetaData:
    """
    Responsible for interacting with Meta Data files:
    - Accessing attributes such as hashes and timestamps ect.
    - Serialize and deserialize from file format.
    - Generate file hash.
    - Generate meta data hash.
    - TODO: Traverse a dataset's history.
    """

    def __init__(self, file_name: str = '') -> None:
        self.parent_hash = None
        self.file_hash = None
        self.cwd = os.getcwd()

        self.file_name = file_name
        self.timestamp = datetime.now()

        self.experiment_id = Theorem().experiment_id

        if file_name != '':
            try:
                with open(file_name, 'r') as f:
                    self.deserialize(f.read())
            except FileNotFoundError:
                raise FileNotFoundError(f"Metadata not found for {file_name}")
            except Exception as e:
                raise Exception(f"Failed to deserialize '{file_name}: {e}' ")

    def serialize(self) -> str:
        """convert MetaData object to json string."""
        return json.dumps(self.__dict__, cls=_ExtendedEncoder)

    def deserialize(self, raw_json: str):
        """convert a json string to MetaData object."""

        json_obj = json.loads(raw_json)

        for k, v in json_obj.items():
            setattr(self, k, v)

        if isinstance(self.timestamp, datetime):
            self.timestamp = datetime.timestamp(self.timestamp)
        else:
            self.timestamp = datetime.fromtimestamp(self.timestamp)

    @dehydratable
    def save(self, destination: str, cwd: str = '',) -> str:
        """perform a serialization and save to file"""

        if cwd == '':
            cwd = self.cwd

        destination = os.path.join(cwd, destination)

        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))

        logging.debug(f"Saving dataset metadata file to: {destination}")
        with open(destination, "w+") as f:
            logging.debug(f"Saving: {destination}")
            f.write(self.serialize())

        return destination

    def get_dir(self):
        raise NotImplementedError()

    def get_latest(self, subdir_path: str = None):

        newest = None
        now = datetime.min

        metadata_dir = subdir_path or self.get_dir()

        for file in os.listdir(metadata_dir):

            # Ignore keep files.
            if cons.KEEP_FILE in file or os.path.isdir(os.path.join(metadata_dir, file)):
                continue

            full_path = os.path.join(metadata_dir, file)

            # Files can be 1 level nested (See Datasets for an example)
            if os.path.isdir(full_path):
                return self.get_latest(full_path)

            dmd = object.__new__(self.__class__)
            self.__class__.__init__(dmd, full_path)

            if dmd.timestamp > now:
                newest = dmd
                now = dmd.timestamp

        return newest


def gen_meta_file_name_from_hash(meta_data_str, file_name, path):
    meta_data_dir = os.path.join(path, make_safe_filename(file_name))
    meta_hash = gen_meta_hash(meta_data_str)
    meta_data_file_name = meta_hash + ".json"

    return os.path.join(meta_data_dir, meta_data_file_name)


def gen_meta_hash(meta_data_str):
    meta_data_file_name = hashlib.sha1()
    meta_data_file_name.update(str.encode(meta_data_str))
    return meta_data_file_name.hexdigest()
