import argparse
import logging
import os
import shutil
import unittest
from uuid import uuid4

from aurum import commands
from tests import run_test_init, set_git_for_test

logging.getLogger().setLevel(logging.DEBUG)


class AddTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.test_dir = f'/tmp/{uuid4()}'
        os.makedirs(self.test_dir)
        self.random_dirs = dict()

        set_git_for_test(self.test_dir)
        run_test_init(selected_dir=self.test_dir)

        f_name = f'{uuid4()}.txt'

        self.relative_path = f_name
        self.absolute_path = os.path.join(self.test_dir, f_name)

        with open(self.absolute_path, 'w') as f:
            f.write("Gibberish")

        self.absolute_path_outside_script = "/tmp/copy.txt"

        with open(self.absolute_path_outside_script, "w") as f:
            f.write("Your text goes here")

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.test_dir)

    def test_add(self):
        parser = argparse.Namespace(files=[
            self.relative_path,
        ])

        files_added = commands.run_add(parser, selected_dir=self.test_dir)
        self.assertEqual(files_added, 1)

        with self.assertRaises(SystemExit):
            commands.run_add(parser, selected_dir='')


if __name__ == '__main__':
    unittest.main()
