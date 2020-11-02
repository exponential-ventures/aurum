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


import argparse
import os
import shutil
import unittest
from uuid import uuid4

from aurum import constants as cons
from aurum import git, commands
from tests import set_git_for_test, run_test_init


class RmTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.repository_path = f"/tmp/{uuid4()}/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)
        set_git_for_test(self.repository_path)
        run_test_init(self.repository_path)

        f_name = f'{uuid4()}.txt'

        self.relative_path = f_name
        self.absolute_path = os.path.join(self.repository_path, f_name)

        with open(self.absolute_path, 'w') as f:
            f.write("Gibberish")

        self.absolute_path_outside_script = f"/tmp/{uuid4()}.txt"

        with open(self.absolute_path_outside_script, "w") as f:
            f.write("Your text goes here")

        self.parser = argparse.Namespace(
            files=[
                self.relative_path,
            ],
            soft_delete=True,
        )
        commands.run_add(self.parser, selected_dir=self.repository_path)

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_rm_from_metadata(self):
        # Assert there is one metadata files, and one .keep
        self.assertEqual(len(os.listdir(os.path.join(self.repository_path, cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))), 2)

        commands.run_rm(self.parser, selected_dir=self.repository_path)

        # Assert there is no metadata files, and just one .keep
        self.assertEqual(len(os.listdir(os.path.join(self.repository_path, cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))), 1)

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
        commands.run_rm(parser, selected_dir=self.repository_path)

    def test_out_of_repo(self):
        with self.assertRaises(FileNotFoundError):
            parser = argparse.Namespace(
                files=[
                    self.absolute_path_outside_script,
                ],
                soft_delete=True,
            )
            commands.run_rm(parser, selected_dir=self.repository_path)


if __name__ == '__main__':
    unittest.main()
