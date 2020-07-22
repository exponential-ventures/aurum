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
from uuid import uuid4

from aurum import commands
from tests import run_test_init, set_git_for_test

logging.getLogger().setLevel(logging.DEBUG)


class AddTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.test_dir = f'/tmp/{uuid4()}'
        os.makedirs(self.test_dir)
        self.random_dirs = dict()

        set_git_for_test(self.test_dir)
        run_test_init(selected_dir=self.test_dir)

        f_name = f'{uuid4()}.txt'

        self.relative_path = f_name
        self.absolute_path = os.path.join(self.test_dir, f_name)

        with open(self.absolute_path, 'w') as f:
            f.write("Gibberish")

        self.absolute_path_outside_script = "/tmp/copy.txt"

        with open(self.absolute_path_outside_script, "w") as f:
            f.write("Your text goes here")

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.test_dir)

    def test_add(self):
        parser = argparse.Namespace(files=[
            self.relative_path,
        ])

        files_added = commands.run_add(parser, selected_dir=self.test_dir)
        self.assertEqual(files_added, 1)

        with self.assertRaises(SystemExit):
            commands.run_add(parser, selected_dir='')


if __name__ == '__main__':
    unittest.main()
