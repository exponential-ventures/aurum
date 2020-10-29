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

import json
import os
import shutil
import unittest
from uuid import uuid4

from aurum import Theorem, load_weights
from aurum.metadata.weights import WeightsMetaData
from tests import set_git_for_test, run_test_init


class TestModel(unittest.TestCase):
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

    def test_save_binary(self):
        magic_d = {'sample_field_a': 'sample value a', 'sample_field_b': 'sample value b'}

        wmd = WeightsMetaData()
        wmd.save_binary(encoded_model=bytes(json.dumps(magic_d), encoding='utf-8'), cwd=self.repository_path)

        self.assertEqual(magic_d, json.loads(wmd.load_binary()))

    def test_save(self):
        magic_d = {'sample_field_a': 'sample value a', 'sample_field_b': 'sample value b'}

        wmd = WeightsMetaData()

        # Force the Theorem to be proven True
        Theorem().code_changed = True

        wmd.model = json.dumps(magic_d)
        dest = wmd.save(cwd=self.repository_path)

        # Assert the metadata file was created and exists
        self.assertTrue(os.path.exists(dest))

        # Assert that the metadata file contains things
        with open(dest, 'r') as f:
            self.assertIsNotNone(f.read())

        # Resetting Theorem to not cross contaminate other tests.
        Theorem().code_changed = False

    def test_load_model(self):
        magic_d = {'sample_field_a': 'sample value a', 'sample_field_b': 'sample value b'}

        wmd = WeightsMetaData()

        # Force the Theorem to be proven True
        Theorem().code_changed = True

        wmd.save_binary(encoded_model=bytes(json.dumps(magic_d), encoding='utf-8'), cwd=self.repository_path)
        dest = wmd.save(cwd=self.repository_path)

        # Assert the metadata file was created and exists
        self.assertTrue(os.path.exists(dest))

        # Assert that the metadata file contains things
        with open(dest, 'r') as f:
            self.assertIsNotNone(f.read())

        # Resetting Theorem to not cross contaminate other tests.
        Theorem().code_changed = False

        encoded_d = load_weights(cwd=self.repository_path)
        self.assertEqual(json.loads(encoded_d), magic_d)


if __name__ == '__main__':
    unittest.main()
