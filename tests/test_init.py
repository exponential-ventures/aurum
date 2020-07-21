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
import shutil
import subprocess
import unittest

from aurum import base
from tests.utils import set_git_for_test


class TestInitMethod(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.repository_path = "/tmp/repository/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.mkdir(self.repository_path)

        # Needed so that we fake as if running from the au repo
        os.chdir(self.repository_path)

        set_git_for_test()

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_init(self):
        original_path = os.getcwd()
        os.chdir(self.repository_path)

        proc = subprocess.Popen(
            ["au -v init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        proc.communicate()

        self.assertEqual(proc.returncode, 0)

        for path in base.get_default_dirs():
            self.assertTrue(path.exists())

        os.chdir(original_path)


if __name__ == '__main__':
    unittest.main()
