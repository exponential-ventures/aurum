#!/usr/bin/env python3
##
# Authors: Adriano Marques
# Nathan Martins
# Thales Ribeiro
##
# Copyright (C) 2019 Exponential Ventures LLC
##
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
##
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
##
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##

import hashlib
import os
import sys
import logging


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


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")


def check_inside_au():
    # TODO: Make sure it will work from wherever it is run
    if not os.path.exists('.au'):
        logging.error(f"Path '.au' does not exist, please run au init \n")
        # sys.exit(1)
