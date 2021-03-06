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

import logging
import os
import random
import shutil
import subprocess
import unittest
from uuid import uuid4

from aurum import constants as cons
from tests import set_git_for_test, run_test_init

logging.getLogger().setLevel(logging.DEBUG)


class AuCommandTestCase(unittest.TestCase):
    """
    Test scenarios:
    -[x] au command is being run the root repository.
    -[x] au command is being run from inside a random inner dir inside the repository.
    -[x] au command is ran outside of the repository to see how it is going to behave.
    -[x] prevent the au command from being run from inside any of the sub-directories of the .au dir.
    """

    def setUp(self) -> None:
        super().setUp()
        self.repository_path = f"/tmp/{uuid4()}/"
        self.random_dirs = dict()

        # Create the root repository
        os.makedirs(self.repository_path)

        set_git_for_test(self.repository_path)
        run_test_init(selected_dir=self.repository_path)

        # Create files at the root of the repository to be added and removed
        for i in range(3):
            path = os.path.join(self.repository_path, f"{i}.txt")

            with open(path, "w+") as tmp_file:
                tmp_file.write("Your text goes here")

        # Create random directories in the root with random files in them.
        for _ in range(3):

            dir_name = str(uuid4())

            path = os.path.join(self.repository_path, dir_name)

            self.random_dirs.update({
                dir_name: path
            })

            os.makedirs(path)

            for i in range(3):
                file_path = os.path.join(path, f"{i}_{dir_name}.txt")
                with open(file_path, "w+") as tmp_file:
                    tmp_file.write("Your text goes here")

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_init(self):

        r = f"/tmp/{uuid4()}/"
        os.mkdir(r)
        set_git_for_test(r)

        proc = subprocess.Popen(
            ["au --verbose init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=r,
        )

        _, e = proc.communicate()

        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.exists(os.path.join(r, cons.REPOSITORY_DIR)))
        shutil.rmtree(r, ignore_errors=True)

    def test_add_from_repo_root(self):

        proc = subprocess.Popen(
            ["au data add 0.txt", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.repository_path,
        )

        o, _ = proc.communicate()

        self.assertEqual(proc.returncode, 0)
        s = "Aurum added the metadata files for the following datasets: 0.txt"
        self.assertIn(s, o.decode(encoding="utf-8"))

    def test_add_from_random_dir_in_repo(self):

        chosen = random.choice(list(self.random_dirs.keys()))
        path = f"0_{chosen}.txt"

        proc = subprocess.Popen(
            [f"au data add {path}", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self.random_dirs[chosen],
        )

        o, e = proc.communicate()

        self.assertEqual(proc.returncode, 0)

        s = f"Aurum added the metadata files for the following datasets: {path}"
        self.assertIn(s, o.decode(encoding="utf-8"))

    def test_add_from_outside_repo(self):

        chosen = random.choice(list(self.random_dirs.keys()))
        path = f"0_{chosen}.txt"

        proc = subprocess.Popen(
            [f"au data add {path}", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd="/tmp/",
        )

        _, e = proc.communicate()

        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"error: You are not running from inside a au repository\n", e)

    def test_add_from_inside_repo_root(self):

        chosen = random.choice(list(self.random_dirs.keys()))
        path = f"0_{chosen}.txt"

        proc = subprocess.Popen(
            [f"au data add {path}", ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=os.path.join(self.repository_path, cons.REPOSITORY_DIR),
        )

        _, e = proc.communicate()

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn(b"does not exist or is not in the repository", e)


if __name__ == '__main__':
    unittest.main()
