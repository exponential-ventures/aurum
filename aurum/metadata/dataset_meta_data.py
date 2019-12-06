import hashlib
import json
import os
from datetime import datetime

from aurum.constants import DATASET_METADATA_DIR
from aurum.metadata import MetaData


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
                self.serialize(f.read())

    def deserialize(self, raw_json: str):
        super().deserialize(raw_json)
        self.timestamp = datetime.fromtimestamp(self.timestamp)

    def save(self, destination: str = None) -> None:

        if destination is None:
            meta_data_str = json.dumps(self.deserialize())
            destination = self.gen_meta_file_name(meta_data_str)

        super().save(destination)

    def gen_file_hash(self):
        sha1 = hashlib.sha1()
        buf_size = 65536  # lets read stuff in 64kb chunks!

        with open(self.file_name, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                sha1.update(data)

        self.file_hash = sha1.hexdigest()

    def gen_meta_file_name(self, meta_data_str):

        meta_data_dir = os.path.join(DATASET_METADATA_DIR, make_safe_filename(self.file_name))

        if not os.path.exists(meta_data_dir):
            os.mkdir(meta_data_dir)

        meta_hash = self.gen_meta_hash(meta_data_str)
        meta_data_file_name = meta_hash + ".json"

        return os.path.join(meta_data_dir, meta_data_file_name)

    @staticmethod
    def gen_meta_hash(meta_data_str):
        meta_data_file_name = hashlib.sha1()
        meta_data_file_name.update(str.encode(meta_data_str))
        return meta_data_file_name.hexdigest()


def get_dataset_metadata(file_name: str) -> (str, DatasetMetaData):
    meta_data_dir = os.path.join(DATASET_METADATA_DIR, make_safe_filename(file_name))

    if os.path.exists(meta_data_dir):
        for mdf in os.listdir(meta_data_dir):

            mdf_path = os.path.join(meta_data_dir, mdf)

            mdo = DatasetMetaData(mdf_path)
            if mdo.file_name == file_name:
                return mdf_path, mdo

    return None, None


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"

    return "".join(safe_char(c) for c in s).rstrip("_")
