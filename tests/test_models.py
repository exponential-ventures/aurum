import shutil
import unittest
import pickle

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

    def test_save_model(self):
        object_to_encode = {
            'sample_field_a': 'sample value a',
            'sample_field_b': 'sample value b'
        }

        au.save_model(pickle.dumps(object_to_encode))
        recovered_data = pickle.loads(au.load_model())

        self.assertEqual(recovered_data['sample_field_a'], object_to_encode['sample_field_a'])


if __name__ == '__main__':
    unittest.main()
