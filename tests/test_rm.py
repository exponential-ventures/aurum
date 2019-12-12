import argparse
import os
import shutil
import unittest

from aurum import base, git, commands
from aurum import constants as cons


class RmTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

        commands.run_init(argparse.Namespace())

        self.relative_path = "README.md"
        self.absolute_path = os.path.abspath("README.md")

        self.absolute_path_outside_script = "/tmp/copy.txt"
        tmp_file = open(self.absolute_path_outside_script, "w")
        tmp_file.write("Your text goes here")
        tmp_file.close()

        self.parser = argparse.Namespace(
            files=[
                self.relative_path,
            ],
            soft_delete=True,
        )
        commands.run_add(self.parser)

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_rm_from_metadata(self):
        # Assert there is one metadata files
        self.assertEqual(len(os.listdir(os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))), 1)

        commands.run_rm(self.parser)

        # Assert there is no metadata files
        self.assertEqual(len(os.listdir(os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR))), 0)

        # Assert files are not in git.
        proc = git.run_git(
            "status"
        )
        proc.wait()
        self.assertNotIn(b"new file:   README.md", proc.stdout.read())

    def test_is_relevant_file(self):
        parser = argparse.Namespace(
            files=[
                self.absolute_path,
                self.relative_path,
            ],
            soft_delete=True,
        )
        commands.run_rm(parser)

        with self.assertRaises(SystemExit):
            parser = argparse.Namespace(
                files=[
                    self.absolute_path_outside_script,
                ],
                soft_delete=True,
            )
            commands.run_rm(parser)


if __name__ == '__main__':
    unittest.main()
