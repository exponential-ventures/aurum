#!/usr/bin/env python3
#
# Authors: Adriano Marques
#          Nathan Martins
#          Thales Ribeiro
#
# Copyright (C) 2019 Exponential Ventures LLC
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Library General Public
#    License as published by the Free Software Foundation; either
#    version 2 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Library General Public License for more details.
#
#    You should have received a copy of the GNU Library General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#


import argparse
import os
import shutil
import subprocess
import unittest
import uuid

from aurum import Theorem, is_new_requirements, end_experiment, commands
from aurum.code_tracker import is_new_code
from tests import set_git_for_test


class LoadTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.repository_path = "/tmp/repository/"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)

        set_git_for_test(self.repository_path)

        Theorem.instance = None

        # Needed so that we fake as if running from the au repo
        os.chdir(self.repository_path)

        proc = subprocess.Popen(
            ["au --verbose init"],
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
            [f"au --verbose data add dataset.txt", ],
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
