import unittest
from datetime import datetime

from aurum.metadata import MetaData


class MetaDataTestCase(unittest.TestCase):

    def test_deserialize(self):
        md = MetaData()
        md.timestamp = datetime(2019, 12, 5, 15, 30)
        md.name = "test"
        raw_json = md.deserialize()
        self.assertEqual(raw_json, '{"timestamp": 1575559800.0, "name": "test"}')

    def test_save(self):
        md = MetaData()
        md.timestamp = datetime(2019, 12, 5, 15, 30)
        md.name = "test"
        md.save("/tmp/a.json")
        with open("/tmp/a.json", 'r') as r:
            self.assertEqual(r.read(), '{"timestamp": 1575559800.0, "name": "test"}')


if __name__ == '__main__':
    unittest.main()
