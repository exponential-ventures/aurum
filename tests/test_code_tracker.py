import logging
import shutil
import tracemalloc
import unittest
from pathlib import Path

from aurum import base
from aurum.commands import run_init
from aurum.code_tracker import is_new_code

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class TestCodeTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        tracemalloc.start()

    @classmethod
    def tearDownClass(cls) -> None:
        tracemalloc.stop()

    def setUp(self) -> None:
        run_init()

    def tearDown(self) -> None:
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_is_new_code_brand_new(self):
        # since the contents haven't changed it should return false.
        self.assertFalse(is_new_code())

    def test_is_new_requirements_adding_requirement(self):
        self.assertFalse(is_new_code())
        Path("src", "test.py").touch()

        # added a new package so this is new.
        self.assertTrue(is_new_code())


if __name__ == '__main__':
    unittest.main()
