import argparse
import os
import shutil
import unittest

from aurum import base, git
from aurum.constants import REPOSITORY_DIR


class RmTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        base.run_init(argparse.Namespace())
        self.file_path = os.path.abspath("README.md")
        self.parser = argparse.Namespace(
            files=[
                self.file_path,

            ],
            soft_delete=True,
        )
        base.run_add(self.parser)

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_rm_from_metadata(self):
        # Assert there is one metadata files
        self.assertEqual(len(os.listdir(REPOSITORY_DIR)), 1)

        base.run_rm(self.parser)

        # Assert there is no metadata files
        self.assertEqual(len(os.listdir(REPOSITORY_DIR)), 0)

        # Assert files are not in git.
        proc = git.run_git(
            "status"
        )
        proc.wait()
        self.assertNotIn(b"new file:   README.md", proc.stdout.read())


if __name__ == '__main__':
    unittest.main()
