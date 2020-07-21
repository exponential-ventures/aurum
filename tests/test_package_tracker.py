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

from aurum import base, git
from aurum import constants as cons
from aurum.commands import run_init
from aurum.package_tracker import is_new_requirements


class PackageTrackerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        run_init()

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_is_new_requirements_brand_new(self):
        # this creates a new metadata file
        is_new, _ = is_new_requirements()
        self.assertTrue(is_new)

        # since the contents haven't changed it should return false.
        is_new, _ = is_new_requirements()
        self.assertFalse(is_new)

    def test_is_new_requirements_adding_requirement(self):
        self.assertTrue(is_new_requirements())
        proc = subprocess.Popen(
            ["pip install minimal", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        o, _ = proc.communicate()

        self.assertEqual(proc.returncode, 0)

        # added a new package so this is new.
        is_new, r_hash = is_new_requirements()
        self.assertTrue(is_new)

        requirements_metadata_dir = \
            os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)

        with open(os.path.join(requirements_metadata_dir, f"{r_hash}.json")) as f:
            self.assertIn("minimal", f.read())


if __name__ == '__main__':
    unittest.main()
