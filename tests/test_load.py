import argparse
import logging
import shutil
import subprocess
import unittest
import uuid

from aurum import commands, base, end_experiment, Theorem, is_new_requirements

logging.getLogger().setLevel(logging.DEBUG)


class LoadTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        for path in base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

        commands.run_init()

        # Creating a new experiment by simply changing the requirements.
        proc = subprocess.Popen(
            ["pip install minimal", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        o, _ = proc.communicate()

        self.assertEqual(proc.returncode, 0)

        b, b_hash = is_new_requirements()

        self.assertTrue(b)

        Theorem().requirements_did_change(b_hash)

        self.experiment_id = Theorem().experiment_id

        self.assertTrue(end_experiment())

    def tearDown(self) -> None:
        super().tearDown()
        for path in base.DEFAULT_DIRS:
            logging.debug(f"Removing dir: {path}")
            shutil.rmtree(path, ignore_errors=True)

    def test_load_unknown_experiment(self):

        cli_result = argparse.Namespace(
            tag=str(uuid.uuid4()),
        )
        with self.assertRaises(Exception):
            commands.run_load(cli_result)

    def test_load_known_experiment(self):

        cli_result = argparse.Namespace(
            tag=self.experiment_id,
        )

        commands.run_load(cli_result)


if __name__ == '__main__':
    unittest.main()
