import argparse
import os
import shutil
import subprocess
import unittest
import uuid
from pathlib import Path

from aurum import Theorem, is_new_requirements, end_experiment, commands
from aurum.code_tracker import is_new_code
from tests.utils import set_git_for_test


class TestExport(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        set_git_for_test()

        self.repository_path = "/tmp/repository/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.mkdir(self.repository_path)

        Theorem.instance = None

        # Needed so that we fake as if running from the au repo
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

        # Creating a new experiment

        # Changing the requirements.
        proc = subprocess.Popen(
            ["pip install minimal", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        o, _ = proc.communicate()

        self.assertEqual(proc.returncode, 0)

        b, b_hash = is_new_requirements()

        self.assertTrue(b)

        # Add code
        with open(os.path.join(self.repository_path, "src/experiment.py"), "w+") as f:
            f.write("print('Hello world')")

        self.assertTrue(is_new_code())

        # Add dataset
        with open(os.path.join(self.repository_path, "dataset.txt"), "w+") as tmp_file:
            tmp_file.write("Your dataset text goes here")

        proc = subprocess.Popen(
            [f"au -v data add dataset.txt", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        out, err = proc.communicate()
        if proc.returncode != 0:
            raise Exception(f"Failed: {err}")

        Theorem().requirements_did_change(b_hash)

        self.experiment_id = Theorem().experiment_id

        self.assertTrue(end_experiment())
        

    def test_export_known_experiment(self):
        cli_result = argparse.Namespace(
            tag=self.experiment_id, no_data=False, no_logs=False, no_metrics=False
        )

        commands.export_experiment(cli_result)
        self.assertTrue(Path(self.repository_path, self.experiment_id + '.zip').exists())


if __name__ == '__main__':
    unittest.main()