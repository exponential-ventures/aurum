import os
import unittest
import shutil
from pathlib import Path
from uuid import uuid4

from aurum.utils import dir_files_by_last_modification_date


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.repository_path = f"/tmp/{uuid4()}"

        # Remove if it exists
        shutil.rmtree(self.repository_path, ignore_errors=True)

        # Create the root repository
        os.makedirs(self.repository_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.repository_path, ignore_errors=True)

    def test_dir_files_by_last_modification_date_desc(self):

        files = [
            'first_file.txt',
            'second_file.txt',
        ]

        for f in files:
            Path(os.path.join(self.repository_path, f)).touch()

        aux = dir_files_by_last_modification_date(self.repository_path)
        self.assertEqual(aux[0][1], f'{self.repository_path}/second_file.txt')
        self.assertEqual(aux[1][1], f'{self.repository_path}/first_file.txt')

    def test_dir_files_by_last_modification_date_asc(self):

        files = [
            'first_file.txt',
            'second_file.txt',
        ]

        for f in files:
            Path(os.path.join(self.repository_path, f)).touch()

        aux = dir_files_by_last_modification_date(self.repository_path, descending_order=False)
        self.assertEqual(aux[0][1], f'{self.repository_path}/first_file.txt')
        self.assertEqual(aux[1][1], f'{self.repository_path}/second_file.txt')
