import unittest
import argparse
import shutil
import sys
import os
import tracemalloc
import subprocess
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


class TestParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tracemalloc.start()
        cls.current_dir = os.getcwd()
        au.base.run_init(argparse.Namespace())

    @classmethod
    def tearDownClass(cls):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

        tracemalloc.stop()

    def test_parameters(self):
        au.parameters(a=1.01, b=333, c=46, epochs=100, batch_size=200)
        self.assertEqual(au.a, 1.01)
        self.assertEqual(au.b, 333)
        self.assertEqual(au.c, 46)
        self.assertEqual(au.epochs, 100)
        self.assertEqual(au.batch_size, 200)

    def test_parameters_from_arg(self):
        args = argparse.Namespace(a=300, b=None, c=None, epochs=None, batch_size=None)
        with patch('aurum.command_line_args', return_value=args):
            au.parameters(a=1.01, b=333, c=46, epochs=100, batch_size=200)
            self.assertEqual(au.a, 300)
            self.assertEqual(au.b, 333)
            self.assertEqual(au.c, 46)
            self.assertEqual(au.epochs, 100)
            self.assertEqual(au.batch_size, 200)

    def test_parameters_from_arg_wo_mock(self):
        proc = subprocess.Popen(
            [f"python3 {self.current_dir}/examples/src/experiment.py -a 40 -epochs 99", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.current_dir,
        )

        output, _ = proc.communicate()

        self.assertTrue(b'a = 40' in output)
        self.assertTrue(b'epochs = 99' in output)

    def test_parameters_with_wrong_argument(self):

        proc = subprocess.Popen(
            [f"python3 {self.current_dir}/examples/src/experiment.py -resga 40", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.current_dir,
        )

        _, error = proc.communicate()
        self.assertTrue(b'error: unrecognized arguments: -resga 40\n' in error)

if __name__ == '__main__':
    unittest.main()
