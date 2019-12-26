import json
import logging
import os
from datetime import datetime

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from .. import git
from ..utils import gen_file_hash, make_safe_filename, dir_files_by_last_modification_date

META_DATA_PATH = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR)


class DatasetMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.size = 0
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        destination = gen_meta_file_name_from_hash(
            meta_data_str=json.dumps(self.serialize()),
            file_name=self.file_name,
            path=META_DATA_PATH
        )

        self.file_hash = gen_file_hash(os.path.join(META_DATA_PATH, self.file_name))

        old_dataset_metadata = get_latest_dataset_metadata()

        if self.file_hash != old_dataset_metadata.file_hash:
            self.parent_hash = old_dataset_metadata.file_hash
            logging.debug(f"Saving dataset metadata file to: {destination}")
            return super().save(destination)


def get_dataset_metadata(file_name: str) -> (str, DatasetMetaData):
    meta_data_dir = os.path.join(META_DATA_PATH, make_safe_filename(file_name))

    for mdf in os.listdir(meta_data_dir):

        mdf_path = os.path.join(meta_data_dir, mdf)

        mdo = DatasetMetaData(mdf_path)

        if mdo.file_name == file_name:
            return mdf_path, mdo

    raise FileNotFoundError(f"Metadata not found for {file_name}")


def get_latest_dataset_metadata() -> DatasetMetaData:
    dataset_metadata_dir = os.path.join(
        git.get_git_repo_root(),
        cons.REPOSITORY_DIR,
        cons.DATASET_METADATA_DIR,
    )

    files = dir_files_by_last_modification_date(dataset_metadata_dir)

    if len(files) > 0:
        return DatasetMetaData(files[0][1])

    return DatasetMetaData()
