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
import logging
import os
import shutil
import unittest

from aurum import base, git, commands
from aurum.constants import REPOSITORY_DIR
from tests.utils import run_test_init, set_git_for_test

logging.getLogger().setLevel(logging.DEBUG)


class AddTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        set_git_for_test()
        run_test_init()
        self.relative_path = "README.md"
        self.absolute_path = os.path.abspath("README.md")

        self.absolute_path_outside_script = "/tmp/copy.txt"
        tmp_file = open(self.absolute_path_outside_script, "w")
        tmp_file.write("Your text goes here")
        tmp_file.close()

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_add(self):
        parser = argparse.Namespace(files=[
            self.relative_path,
        ])
        commands.run_add(parser)

        proc = git.run_git(
            "status"
        )

        self.assertEqual(proc.wait(), 0)
        prod_res = proc.stdout.read()

        self.assertIn(b"new file:   README.md", prod_res)


    def test_is_relevant_file(self):
        parser = argparse.Namespace(files=[
            self.absolute_path,
            self.relative_path,
        ])
        commands.run_add(parser)

        with self.assertRaises(SystemExit):
            parser = argparse.Namespace(files=[
                self.absolute_path_outside_script,
            ])
            commands.run_add(parser)


if __name__ == '__main__':
    unittest.main()
