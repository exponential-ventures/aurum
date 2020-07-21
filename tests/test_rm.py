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


import argparse
import os
import shutil
import unittest

from aurum import base, git, commands
from aurum import constants as cons


class RmTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

        commands.run_init()

        self.relative_path = "README.md"
        self.absolute_path = os.path.abspath("README.md")

        self.absolute_path_outside_script = "/tmp/copy.txt"
        tmp_file = open(self.absolute_path_outside_script, "w")
        tmp_file.write("Your text goes here")
        tmp_file.close()

        self.parser = argparse.Namespace(
            files=[
                self.relative_path,
            ],
            soft_delete=True,
        )
        commands.run_add(self.parser)

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_rm_from_metadata(self):
        # Assert there is one metadata files, and one .keep
        self.assertEqual(len(os.listdir(os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))), 2)

        commands.run_rm(self.parser)

        # Assert there is no metadata files, and just one .keep
        self.assertEqual(len(os.listdir(os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))), 1)

        # Assert files are not in git.
        proc = git.run_git(
            "status"
        )
        proc.wait()
        self.assertNotIn(b"new file:   README.md", proc.stdout.read())

    def test_is_relevant_file(self):
        parser = argparse.Namespace(
            files=[
                self.relative_path,
            ],
            soft_delete=True,
        )
        commands.run_rm(parser)

    def test_out_of_repo(self):

        with self.assertRaises(SystemExit):
            parser = argparse.Namespace(
                files=[
                    self.absolute_path_outside_script,
                ],
                soft_delete=True,
            )
            commands.run_rm(parser)


if __name__ == '__main__':
    unittest.main()
