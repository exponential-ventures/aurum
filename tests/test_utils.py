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
import unittest
import shutil
from pathlib import Path
from uuid import uuid4

from aurum.utils import dir_files_by_last_modification_date


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.repository_path = f"/tmp/{uuid4()}"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_dir_files_by_last_modification_date_desc(self):

        files = [
            'first_file.txt',
            'second_file.txt',
        ]

        for f in files:
            Path(os.path.join(self.repository_path, f)).touch()

        aux = dir_files_by_last_modification_date(self.repository_path)
        self.assertEqual(aux[0][1], f'{self.repository_path}/second_file.txt')
        self.assertEqual(aux[1][1], f'{self.repository_path}/first_file.txt')

    def test_dir_files_by_last_modification_date_asc(self):

        files = [
            'first_file.txt',
            'second_file.txt',
        ]

        for f in files:
            Path(os.path.join(self.repository_path, f)).touch()

        aux = dir_files_by_last_modification_date(self.repository_path, descending_order=False)
        self.assertEqual(aux[0][1], f'{self.repository_path}/first_file.txt')
        self.assertEqual(aux[1][1], f'{self.repository_path}/second_file.txt')
