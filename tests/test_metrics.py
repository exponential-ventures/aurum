import logging
import os
import shutil
import unittest
from uuid import uuid4

import aurum as au
from aurum import constants as cons
from aurum.metadata.metrics import MetricsMetaData
from tests import set_git_for_test, run_test_init

logging.getLogger().setLevel(logging.DEBUG)


class TestMetrics(unittest.TestCase):
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

    def test_register_metrics(self):
        au.register_metrics(resga=800, foo=2_000, cwd=self.repository_path)
        metrics_metadata = MetricsMetaData().get_latest(
            os.path.join(self.repository_path, cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))
        self.assertEqual(metrics_metadata.metrics['resga'], 800)
        self.assertEqual(metrics_metadata.metrics['foo'], 2_000)
        self.assertTrue('environment' in metrics_metadata.metrics)
        self.assertTrue('hardware' in metrics_metadata.metrics)


if __name__ == '__main__':
    unittest.main()
