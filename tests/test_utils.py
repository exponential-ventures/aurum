import unittest
import shutil
from pathlib import Path

from aurum.utils import dir_files_by_last_modification_date


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.dir_path = Path('tests', 'dir')
        if not self.dir_path.exists():
            self.dir_path.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir_path, ignore_errors=True)

    def test_dir_files_by_last_modification_date_desc(self):
        Path('tests', 'dir', 'first_file.txt').touch()
        Path('tests', 'dir', 'second_file.txt').touch()
        aux = dir_files_by_last_modification_date(self.dir_path)
        self.assertEqual(aux[0][1], f'{self.dir_path}/second_file.txt')
        self.assertEqual(aux[1][1], f'{self.dir_path}/first_file.txt')

    def test_dir_files_by_last_modification_date_asc(self):
        Path('tests', 'dir', 'first_file.txt').touch()
        Path('tests', 'dir', 'second_file.txt').touch()
        aux = dir_files_by_last_modification_date(self.dir_path, descending_order=False)
        self.assertEqual(aux[0][1], f'{self.dir_path}/first_file.txt')
        self.assertEqual(aux[1][1], f'{self.dir_path}/second_file.txt')
