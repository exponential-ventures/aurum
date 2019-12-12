import hashlib
import json
import os
from datetime import datetime

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.utils import gen_file_hash, make_safe_filename


class DatasetMetaData(MetaData):
    """
    Responsible for interacting with Meta Data files:
    - Accessing attributes such as hashes and timestamps ect.
    - Serialize and deserialize from file format.
    - Generate file hash.
    - Generate meta data hash.
    - Generate meta data file name.
    - TODO: Traverse a dataset's history.
    """

    def __init__(self, file_name: str = '') -> None:
        self.file_name = file_name
        self.file_hash = None
        self.parent_hash = None
        self.size = 0
        self.timestamp = datetime.now()

        if file_name != '':
            with open(file_name, 'r') as f:
                self.deserialize(f.read())

    def deserialize(self, raw_json: str):
        super().deserialize(raw_json)
        self.timestamp = datetime.fromtimestamp(self.timestamp)

    def save(self, destination: str = None) -> str:

        if destination is None:
            meta_data_str = json.dumps(self.serialize())
            destination = gen_meta_file_name(meta_data_str, self.file_name)

        if self.file_hash is None:
            # this file path must be absolute
            self.file_hash = gen_file_hash(os.path.join(git.get_git_repo_root(), self.file_name))
      
        return super().save(destination)


def get_dataset_metadata(file_name: str) -> (str, DatasetMetaData):
    meta_data_dir = os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR, make_safe_filename(file_name))

    if os.path.exists(meta_data_dir):
        for mdf in os.listdir(meta_data_dir):

            mdf_path = os.path.join(meta_data_dir, mdf)

            mdo = DatasetMetaData(mdf_path)
            if mdo.file_name == file_name:
                return mdf_path, mdo

    return None, None


def gen_meta_hash(meta_data_str):
    meta_data_file_name = hashlib.sha1()
    meta_data_file_name.update(str.encode(meta_data_str))
    return meta_data_file_name.hexdigest()


def gen_meta_file_name(meta_data_str, file_name):
    path = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, "datasets")

    meta_data_dir = os.path.join(path, make_safe_filename(file_name))

    if not os.path.exists(meta_data_dir):
        os.mkdir(meta_data_dir)

    meta_hash = gen_meta_hash(meta_data_str)
    meta_data_file_name = meta_hash + ".json"

    return os.path.join(meta_data_dir, meta_data_file_name)
