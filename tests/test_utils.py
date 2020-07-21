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


import unittest
import shutil
from pathlib import Path

from aurum.utils import dir_files_by_last_modification_date


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.dir_path = Path('tests', 'dir')
        if not self.dir_path.exists():
            self.dir_path.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir_path, ignore_errors=True)

    def test_dir_files_by_last_modification_date_desc(self):
        Path('tests', 'dir', 'first_file.txt').touch()
        Path('tests', 'dir', 'second_file.txt').touch()
        aux = dir_files_by_last_modification_date(self.dir_path)
        self.assertEqual(aux[0][1], f'{self.dir_path}/second_file.txt')
        self.assertEqual(aux[1][1], f'{self.dir_path}/first_file.txt')

    def test_dir_files_by_last_modification_date_asc(self):
        Path('tests', 'dir', 'first_file.txt').touch()
        Path('tests', 'dir', 'second_file.txt').touch()
        aux = dir_files_by_last_modification_date(self.dir_path, descending_order=False)
        self.assertEqual(aux[0][1], f'{self.dir_path}/first_file.txt')
        self.assertEqual(aux[1][1], f'{self.dir_path}/second_file.txt')
