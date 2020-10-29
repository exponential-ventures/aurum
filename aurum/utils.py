#!/usr/bin/env python3
#
# Authors: Adriano Marques
#          Nathan Martins
#          Thales Ribeiro
#
# Copyright (C) 2019 Exponential Ventures LLC
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Library General Public
#    License as published by the Free Software Foundation; either
#    version 2 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Library General Public License for more details.
#
#    You should have received a copy of the GNU Library General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

import errno
import hashlib
import json
import logging
import os
import shutil
import sys
import time
import urllib.request
from collections import OrderedDict

from . import constants as cons
from . import git


def gen_file_hash(file_name):
    sha1 = hashlib.sha1()
    buf_size = 65536  # lets read stuff in 64kb chunks!

    with open(file_name, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def gen_dict_hash(dictionary: dict) -> str:
    if not isinstance(dictionary, dict):
        raise TypeError('Parameter provided is not a dictionary')

    sha1 = hashlib.sha1()
    ordered_dict = OrderedDict(dictionary.items())
    sha1.update(json.dumps(ordered_dict).encode('utf-8'))
    return sha1.hexdigest()


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")


def size_in_gb(size):
    return f"{size / float(1 << 30)} GB"


def check_inside_au():
    path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR)
    if not os.path.exists(path):
        logging.error(f"Path '.au' does not exist, please run au init \n")
        sys.exit(1)


def dic_to_str(dictionary: dict, title: str = None) -> str:
    aux_str = ""
    if title:
        aux_str += f"\n {title}"
    for k, v in sorted(dictionary.items()):
        if isinstance(v, dict):
            aux_str += dic_to_str(v, k)
        else:
            aux_str += f"\n\t {k}={v}"
    aux_str += "\n"
    return aux_str


def did_dict_change(d1, d2):
    """
    Compares two dict to detect if the first has any changes against the second.
    In case of any changes it returns True. Otherwise, it returns false.
    """
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


def dir_files_by_last_modification_date(directory_path: str, descending_order: bool = True) -> list:
    file_last_modified_list = []

    for f in os.listdir(directory_path):
        if cons.KEEP_FILE not in f:
            file_path = os.path.join(directory_path, f)
            stats = os.stat(file_path)
            lastmod_date = time.localtime(stats[8])
            file_last_modified_list.append((lastmod_date, file_path))

    file_last_modified_list.sort()

    if descending_order:
        file_last_modified_list.reverse()  # The first is the latest modified

    return file_last_modified_list


def copy_dir_and_files(source, destiny):
    try:
        shutil.copytree(source, destiny)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(source, destiny)
        else:
            logging.error(f'Directory not copied, error: {e}')


def download_file_from_web(url: str, output: str) -> None:
    with urllib.request.urlopen(url) as response, open(output, 'wb') as f:
        shutil.copyfileobj(response, f)
