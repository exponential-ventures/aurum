import shutil
import unittest

import aurum as au
from aurum.metadata.metrics import MetricsMetaData


class TestMetrics(unittest.TestCase):
    def setUp(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        au.base.run_init()

    def tearDown(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_register_metrics(self):
        au.register_metrics(resga=800, foo=2_000)
        metrics_metadata = MetricsMetaData().get_latest()
        self.assertEqual(metrics_metadata.metrics['resga'], 800)
        self.assertEqual(metrics_metadata.metrics['foo'], 2_000)
        self.assertTrue('environment' in metrics_metadata.metrics)
        self.assertTrue('hardware' in metrics_metadata.metrics)


if __name__ == '__main__':
    unittest.main()
