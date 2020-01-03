import logging
import os
import shutil
import subprocess
import unittest

from aurum import use_datasets
from aurum.dataset_tracker import DatasetTracker, is_new_dataset


class DatasetTrackerCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.repository_path = "/tmp/repository/"
        # Create the root repository
        os.mkdir(self.repository_path)
        test_run_init()

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
        use_datasets(self.ds)
        self.assertIn(self.ds, DatasetTracker().datasets)

        # No previous experiment run, so it should be true
        is_new, h = is_new_dataset()
        self.assertTrue(is_new)
        self.assertIsInstance(h, str)


def test_run_init(repository_path: str = "/tmp/repository/"):
    proc = subprocess.Popen(
        ["au -v init"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=repository_path,
    )

    _, e = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"Unable to run init. {e} {proc.returncode}")

    logging.debug("test_run_init ran successfully")


if __name__ == '__main__':
    unittest.main()
