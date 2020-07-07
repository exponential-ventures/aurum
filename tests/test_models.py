import json
import os
import shutil
import unittest

import aurum as au
from aurum import Theorem
from aurum.metadata.model import ModelMetaData


class TestModel(unittest.TestCase):
    def setUp(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        au.base.run_init()

    def tearDown(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_save_binary(self):

        path = "/tmp/model.o"
        magic_d = {'sample_field_a': 'sample value a', 'sample_field_b': 'sample value b'}

        mmd = ModelMetaData()

        mmd.model = json.dumps(magic_d)
        mmd.save_binary(path)

        self.assertEqual(magic_d, json.loads(mmd.load_binary(path)))

    def test_save(self):

        magic_d = {'sample_field_a': 'sample value a', 'sample_field_b': 'sample value b'}

        mmd = ModelMetaData()

        # Force the Theorem to be proven True
        Theorem().code_changed = True

        mmd.model = json.dumps(magic_d)
        dest = mmd.save()

        # Assert the metadata file was created and exists
        self.assertTrue(os.path.exists(dest))

        # Assert that the metadata file contains things
        with open(dest, 'r') as f:
            self.assertIsNotNone(f.read())

        # Resetting Theorem to not cross contaminate other tests.
        Theorem().code_changed = False


if __name__ == '__main__':
    unittest.main()
