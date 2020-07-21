import unittest
from datetime import datetime

from aurum.metadata import MetaData


class MetaDataTestCase(unittest.TestCase):

    def test_serialize(self):
        md = MetaData()
        md.timestamp = datetime(2019, 12, 5, 15, 30)
        md.name = "test"
        raw_json = md.serialize()
        self.assertEqual(
            raw_json,
            f'{{"parent_hash": null, "file_hash": null, "cwd": "/tmp/repository", "file_name": "", "timestamp": 1575559800.0, '
            f'"experiment_id": "{md.experiment_id}", "name": "test"}}'
        )

    def test_save(self):
        md = MetaData()
        md.timestamp = datetime(2019, 12, 5, 15, 30)
        md.name = "test"
        md.save("/tmp/a.json")
        with open("/tmp/a.json", 'r') as r:
            self.assertEqual(
                r.read(),
                f'{{"parent_hash": null, "file_hash": null, "cwd": "/tmp/repository", "file_name": "", "timestamp": 1575559800.0, '
                f'"experiment_id": "{md.experiment_id}", "name": "test"}}'
            )


if __name__ == '__main__':
    unittest.main()
