import unittest
import argparse
import shutil
import sys
import tracemalloc

try:
    import aurum as au
    from aurum.constants import REPOSITORY_DIR
    from aurum.metadata import load_metrics
except ImportError:
    import sys

    sys.path.append("../aurum")
    import aurum as au
    from aurum.constants import REPOSITORY_DIR
    from aurum.metadata import load_metrics


class TestMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        tracemalloc.start()
        au.base.run_init(argparse.Namespace())

    @classmethod
    def tearDownClass(cls):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

        tracemalloc.stop()

    def test_register_metrics(self):
        au.register_metrics(resga=800, foo=2_000)
        metrics = load_metrics()
        self.assertEqual(metrics['resga'], 800)
        self.assertEqual(metrics['foo'], 2_000)
        self.assertTrue('environment' in metrics)
        self.assertTrue('hardware' in metrics)


if __name__ == '__main__':
    unittest.main()
