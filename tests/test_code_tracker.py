import shutil
import unittest
from pathlib import Path

from aurum import base
from aurum.code_tracker import is_new_code
from aurum.commands import run_init


class TestCodeTracker(unittest.TestCase):

    def setUp(self) -> None:
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        run_init()

    def tearDown(self) -> None:
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_is_new_code_brand_new(self):
        is_new, _ = is_new_code()
        self.assertTrue(is_new)

    def test_is_new_requirements_adding_requirement(self):

        path = Path("src", "test.py")
        path.touch()

        # added a new package so this is new.
        is_new, _ = is_new_code()
        self.assertTrue(is_new)

        # should be false because there isn't any change
        is_new, _ = is_new_code()
        self.assertFalse(is_new)

        with open(path, 'w+') as f:
            f.write('print(foo)')

        is_new, _ = is_new_code()
        self.assertTrue(is_new)


if __name__ == '__main__':
    unittest.main()
