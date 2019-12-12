import unittest
import argparse
import shutil
import sys
import tracemalloc
from io import StringIO
from unittest.mock import patch

try:
    import aurum as au
    from aurum.constants import REPOSITORY_DIR
except ImportError:
    import sys

    sys.path.append("../aurum")
    import aurum as au
    from aurum.constants import REPOSITORY_DIR


class TestMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        tracemalloc.start()
        au.base.run_init(argparse.Namespace())

    @classmethod
    def tearDownClass(cls):
        # for path in au.base.DEFAULT_DIRS:
        #     shutil.rmtree(path, ignore_errors=True)

        tracemalloc.stop()

    def test_register_metrics(self):
        au.register_metrics(resga=800)

    # def test_parameters_from_arg(self):
    #     args = argparse.Namespace(a=300)
    #     with patch('aurum.command_line_args', return_value=args):
    #         au.parameters(a=1.01, b=333, c=46, epochs=100, batch_size=200)
    #         self.assertEqual(au.a, 300)
    #         self.assertEqual(au.b, 333)
    #         self.assertEqual(au.c, 46)
    #         self.assertEqual(au.epochs, 100)
    #         self.assertEqual(au.batch_size, 200)


if __name__ == '__main__':
    unittest.main()
