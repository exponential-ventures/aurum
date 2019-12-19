import logging
import shutil
import tracemalloc
import unittest

import aurum as au
from aurum.metadata.metrics import get_latest_metrics_metadata

logging.getLogger().setLevel(logging.DEBUG)


class TestMetrics(unittest.TestCase):
    def setUp(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        tracemalloc.start()
        au.base.run_init()

    def tearDown(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

        tracemalloc.stop()

    def test_register_metrics(self):
        au.register_metrics(resga=800, foo=2_000)
        metrics = get_latest_metrics_metadata()
        self.assertEqual(metrics.metrics['resga'], 800)
        self.assertEqual(metrics.metrics['foo'], 2_000)
        self.assertTrue('environment' in metrics.metrics.keys())
        self.assertTrue('hardware' in metrics.metrics.keys())


if __name__ == '__main__':
    unittest.main()
