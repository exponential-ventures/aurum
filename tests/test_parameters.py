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


import os
import shutil
import subprocess
import unittest
from uuid import uuid4

import aurum as au
from tests import set_git_for_test, run_test_init


class TestParameters(unittest.TestCase):
    def setUp(self):
        self.repository_path = f"/tmp/{uuid4()}/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)
        set_git_for_test(self.repository_path)
        run_test_init(self.repository_path)

    def tearDown(self):
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_parameters(self):
        au.parameters(
            cwd=self.repository_path,
            a=1.01,
            b=333,
            c=46,
            epochs=100,
            batch_size=200,
            unsafe_parameter_checking=True,
        )
        self.assertEqual(au.a, 1.01)
        self.assertEqual(au.b, 333)
        self.assertEqual(au.c, 46)
        self.assertEqual(au.epochs, 100)
        self.assertEqual(au.batch_size, 200)

    def test_parameters_from_arg_wo_mock(self):
        shutil.copyfile('/usr/src/app/tests/mock/parameters.py', os.path.join(self.repository_path, "parameters.py"))

        proc = subprocess.Popen(
            [f"python3 {self.repository_path}parameters.py -a 40 -epochs 99"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        output, error = proc.communicate()
        self.assertEqual(proc.returncode, 0)

        self.assertTrue(b'a = 40' in output)
        self.assertTrue(b'epochs = 99' in output)


if __name__ == '__main__':
    unittest.main()
