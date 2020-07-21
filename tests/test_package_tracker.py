import logging
import os
import shutil
import subprocess
import unittest
from uuid import uuid4

from aurum import constants as cons
from aurum.package_tracker import is_new_requirements
from tests import set_git_for_test, run_test_init

logging.getLogger().setLevel(logging.DEBUG)


class PackageTrackerTestCase(unittest.TestCase):

    def setUp(self):
        self.repository_path = f"/tmp/{uuid4()}/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)
        set_git_for_test(self.repository_path)
        run_test_init(self.repository_path)

    def tearDown(self):
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_is_new_requirements_brand_new(self):
        # this creates a new metadata file
        is_new, _ = is_new_requirements(cwd=self.repository_path)
        self.assertTrue(is_new)

        # since the contents haven't changed it should return false.
        is_new, _ = is_new_requirements(cwd=self.repository_path)
        self.assertFalse(is_new)

    def test_is_new_requirements_adding_requirement(self):

        # Other tests cross contaminate the global packages since we are not
        # using virtual envs.
        proc = subprocess.run(
            "pip uninstall minimal -y",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        self.assertEqual(proc.returncode, 0)

        self.assertTrue(is_new_requirements(cwd=self.repository_path))
        proc = subprocess.Popen(
            ["pip install minimal", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        o, _ = proc.communicate()

        self.assertEqual(proc.returncode, 0)

        # added a new package so this is new.
        is_new, r_hash = is_new_requirements(cwd=self.repository_path)
        self.assertTrue(is_new)

        requirements_metadata_dir = os.path.join(self.repository_path, cons.REPOSITORY_DIR,
                                                 cons.REQUIREMENTS_METADATA_DIR)

        with open(os.path.join(requirements_metadata_dir, f"{r_hash}.json")) as f:
            self.assertIn("minimal", f.read())


if __name__ == '__main__':
    unittest.main()
