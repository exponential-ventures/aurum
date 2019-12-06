import argparse
import os
import shutil
import unittest

from aurum import base, git
from aurum.constants import REPOSITORY_DIR


class AddTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        base.run_init(argparse.Namespace())
        self.file_path = os.path.abspath("README.md")

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_add(self):
        parser = argparse.Namespace(files=[
            self.file_path,
        ])
        base.run_add(parser)

        proc = git.run_git(
            "status"
        )

        self.assertEqual(proc.wait(), 0)
        prod_res = proc.stdout.read()

        self.assertIn(b"new file:   README.md", prod_res)

        meta_data_file_path = os.path.join(REPOSITORY_DIR, os.listdir(REPOSITORY_DIR)[0])
        meta_data_assert = f'new file:   {meta_data_file_path}'
        self.assertIn(str.encode(meta_data_assert), prod_res)


if __name__ == '__main__':
    unittest.main()
