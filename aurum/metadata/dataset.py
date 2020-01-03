import json
import logging
import os
from datetime import datetime

from .metadata import MetaData, gen_meta_file_name_from_hash
from .. import constants as cons
from .. import git
from ..utils import gen_file_hash, make_safe_filename


class DatasetMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        super().__init__(file_name)
        self.size = 0

    def save(self, destination: str = None) -> str:
        meta_data_path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR)
        destination = gen_meta_file_name_from_hash(
            meta_data_str=json.dumps(self.serialize()),
            file_name=self.file_name,
            path=meta_data_path,
        )

        self.file_hash = gen_file_hash(os.path.join(git.get_git_repo_root(), self.file_name))

        old_dataset_metadata = DatasetMetaData().get_latest()

        if old_dataset_metadata and self.file_hash != old_dataset_metadata.file_hash:
            self.parent_hash = old_dataset_metadata.file_hash

        logging.debug(f"Saving dataset metadata file to: {destination}")
        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            git.get_git_repo_root(),
            cons.REPOSITORY_DIR,
            cons.DATASET_METADATA_DIR,
        )


def get_dataset_metadata(file_name: str) -> (str, DatasetMetaData):
    meta_data_path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR)

    meta_data_dir = os.path.join(meta_data_path, make_safe_filename(file_name))

    for mdf in os.listdir(meta_data_dir):

        mdf_path = os.path.join(meta_data_dir, mdf)

        mdo = DatasetMetaData(mdf_path)

        if mdo.file_name == file_name:
            return mdf_path, mdo

    raise FileNotFoundError(f"Metadata not found for {file_name}")


