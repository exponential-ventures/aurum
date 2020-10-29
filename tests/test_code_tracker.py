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

import shutil
import unittest
from pathlib import Path

from aurum import base
from aurum.code_tracker import is_new_code
from aurum.commands import run_init


class TestCodeTracker(unittest.TestCase):

    def setUp(self) -> None:

        self.default_dirs = base.get_default_dirs()

        for path in self.default_dirs:
            shutil.rmtree(path, ignore_errors=True)
        run_init()

    def tearDown(self) -> None:
        for path in self.default_dirs:
            shutil.rmtree(path, ignore_errors=True)

    def test_is_new_code_brand_new(self):
        is_new, _ = is_new_code()
        self.assertTrue(is_new)

    def test_is_new_requirements_adding_requirement(self):

        path = Path("src", "test.py")
        path.touch()

        # added a new package so this is new.
        is_new, _ = is_new_code()
        self.assertTrue(is_new)

        # should be false because there isn't any change
        is_new, _ = is_new_code()
        self.assertFalse(is_new)

        with open(path, 'w+') as f:
            f.write('print(foo)')

        is_new, _ = is_new_code()
        self.assertTrue(is_new)


if __name__ == '__main__':
    unittest.main()
