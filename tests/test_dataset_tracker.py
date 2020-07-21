import logging
import os
import shutil
import subprocess
import unittest
from uuid import uuid4

from aurum import use_datasets
from aurum.dataset_tracker import DatasetTracker, is_new_dataset
from tests import set_git_for_test, run_test_init


class DatasetTrackerCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        # Create the root repository
        self.repository_path = f"/tmp/{uuid4()}/"
        os.makedirs(self.repository_path)
        set_git_for_test(self.repository_path)
        run_test_init(selected_dir=self.repository_path)

        self.ds = f"dataset.txt"

        file_path = os.path.join(self.repository_path, self.ds)
        with open(file_path, "w+") as tmp_file:
            tmp_file.write("Your dataset text goes here")

        proc = subprocess.Popen(
            [f"au data add {self.ds}", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        out, err = proc.communicate()
        if proc.returncode != 0:
            raise Exception(f"Failed: {err}, {out}, {proc.returncode}")
        else:
            logging.debug(f"au data add worked...{out}")

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_use_datasets(self):

        # Needed so that we fake as if running from the au repo
        os.chdir(self.repository_path)
        use_datasets(self.ds, cwd=self.repository_path)
        self.assertIn(self.ds, DatasetTracker().datasets)

        # No previous experiment run, so it should be true
        is_new, h = is_new_dataset(self.repository_path)
        self.assertTrue(is_new)
        self.assertIsInstance(h, str)


if __name__ == '__main__':
    unittest.main()
