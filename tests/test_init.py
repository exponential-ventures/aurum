import shutil
import unittest

from aurum import commands, base


class TestInitMethod(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_init(self):
        commands.au_init()
        for path in base.DEFAULT_DIRS:
            self.assertTrue(path.exists())


if __name__ == '__main__':
    unittest.main()
