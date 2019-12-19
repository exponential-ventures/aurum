import logging
import shutil
import subprocess
import unittest

from aurum import base
from aurum.commands import run_init
from aurum.package_tracker import is_new_requirements

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class PackageTrackerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        run_init()

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_is_new_requirements_brand_new(self):
        # this creates a new metadata file
        self.assertTrue(is_new_requirements())

        # since the contents haven't changed it should return false.
        self.assertFalse(is_new_requirements())

    def test_is_new_requirements_adding_requirement(self):
        self.assertTrue(is_new_requirements())
        proc = subprocess.Popen(
            ["pip install minimal", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        o, _ = proc.communicate()

        self.assertEqual(proc.returncode, 0)

        # added a new package so this is new.
        self.assertTrue(is_new_requirements())


if __name__ == '__main__':
    unittest.main()
