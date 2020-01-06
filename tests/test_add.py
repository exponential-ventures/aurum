import argparse
import logging
import os
import shutil
import unittest

from aurum import base, git, commands
from aurum.constants import REPOSITORY_DIR
from tests.utils import run_test_init, set_git_for_test

logging.getLogger().setLevel(logging.DEBUG)


class AddTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        set_git_for_test()
        run_test_init()
        self.relative_path = "README.md"
        self.absolute_path = os.path.abspath("README.md")

        self.absolute_path_outside_script = "/tmp/copy.txt"
        tmp_file = open(self.absolute_path_outside_script, "w")
        tmp_file.write("Your text goes here")
        tmp_file.close()

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_add(self):
        parser = argparse.Namespace(files=[
            self.relative_path,
        ])
        commands.run_add(parser)

        proc = git.run_git(
            "status"
        )

        self.assertEqual(proc.wait(), 0)
        prod_res = proc.stdout.read()

        self.assertIn(b"new file:   README.md", prod_res)


    def test_is_relevant_file(self):
        parser = argparse.Namespace(files=[
            self.absolute_path,
            self.relative_path,
        ])
        commands.run_add(parser)

        with self.assertRaises(SystemExit):
            parser = argparse.Namespace(files=[
                self.absolute_path_outside_script,
            ])
            commands.run_add(parser)


if __name__ == '__main__':
    unittest.main()
