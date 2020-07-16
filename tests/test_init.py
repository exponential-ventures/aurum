import os
import shutil
import subprocess
import unittest

from aurum import base
from tests.utils import set_git_for_test


class TestInitMethod(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.repository_path = "/tmp/repository/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)

        # Needed so that we fake as if running from the au repo
        os.chdir(self.repository_path)

        set_git_for_test()

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_init(self):
        original_path = os.getcwd()
        os.chdir(self.repository_path)

        proc = subprocess.Popen(
            ["au -v init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        proc.communicate()

        self.assertEqual(proc.returncode, 0)

        for path in base.get_default_dirs():
            self.assertTrue(path.exists())

        os.chdir(original_path)


if __name__ == '__main__':
    unittest.main()
