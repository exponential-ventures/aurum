import json
import shutil
import unittest

import aurum as au
from aurum.metadata.model import ModelMetaData


class TestModel(unittest.TestCase):
    def setUp(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        au.base.run_init()

    def tearDown(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_save(self):

        path = "/tmp/model.o"
        magic_d = {'sample_field_a': 'sample value a', 'sample_field_b': 'sample value b'}

        mmd = ModelMetaData()

        mmd.model = json.dumps(magic_d)
        mmd.save_binary(path)

        self.assertEqual(magic_d, json.loads(mmd.load_binary(path)))


if __name__ == '__main__':
    unittest.main()
