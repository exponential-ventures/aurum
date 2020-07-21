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

import aurum as au


class TestParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current_dir = os.getcwd()

        au.base.run_init()

    @classmethod
    def tearDownClass(cls):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_parameters(self):
        au.parameters(a=1.01, b=333, c=46, epochs=100, batch_size=200)
        self.assertEqual(au.a, 1.01)
        self.assertEqual(au.b, 333)
        self.assertEqual(au.c, 46)
        self.assertEqual(au.epochs, 100)
        self.assertEqual(au.batch_size, 200)

    def test_parameters_from_arg_wo_mock(self):
        proc = subprocess.Popen(
            [f"python3 {self.current_dir}/examples/src/experiment.py -a 40 -epochs 99", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.current_dir,
        )

        output, error = proc.communicate()

        self.assertTrue(b'a = 40' in output)
        self.assertTrue(b'epochs = 99' in output)


if __name__ == '__main__':
    unittest.main()
