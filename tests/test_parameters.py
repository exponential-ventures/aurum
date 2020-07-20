import os
import shutil
import subprocess
import unittest
import tracemalloc

import aurum as au


class TestParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current_dir = os.getcwd()
        tracemalloc.start()

        au.base.run_init()

    @classmethod
    def tearDownClass(cls):
        tracemalloc.stop()
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_parameters(self):
        au.parameters(a=1.01, b=333, c=46, epochs=100, batch_size=200)
        self.assertEqual(au.a, 1.01)
        self.assertEqual(au.b, 333)
        self.assertEqual(au.c, 46)
        self.assertEqual(au.epochs, 100)
        self.assertEqual(au.batch_size, 200)

    def test_parameters_from_arg_wo_mock(self):
        proc = subprocess.Popen(
            [f"python3 {self.current_dir}/tests/utils/parameters.py -a 40 -epochs 99" ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.current_dir,
        )

        output, error = proc.communicate()

        self.assertTrue(b'a = 40' in output)
        self.assertTrue(b'epochs = 99' in output)


if __name__ == '__main__':
    unittest.main()
