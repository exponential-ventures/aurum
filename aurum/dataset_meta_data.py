import hashlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DatasetMetaData:
    """
    Responsible for interacting with Meta Data files:
    - Accessing attributes such as hashes and timestamps ect.
    - Serialize and deserialize from file format.
    - Generate file hash.
    - Generate meta data hash.
    - Generate meta data file name.
    - TODO: Traverse a dataset's history.
    """

    file_hash: str = None
    parent_hash: str = None
    file_name: str = None
    size: int = 0
    timestamp: datetime = datetime.now()

    def __init__(self, file_name: str = '') -> None:
        self.file_name = file_name

        if file_name != '':
            with open(file_name, 'r') as f:
                self.serialize(f.read())

    def serialize(self, raw_meta_data: str):
        """
        This method takes in a raw string and attempts to parse it into a meta data object.
        """
        so = json.loads(raw_meta_data)
        self.file_name = so.get("file_name")
        self.timestamp = so.get("timestamp")
        self.size = so.get("size")
        self.file_hash = so.get("hash")
        self.parent_hash = so.get("parent_hash")

    def deserialize(self) -> str:
        """
        This method saves the Meta Data to a file.
        Returns the path to the saved location
        """

        meta_data = {
            "file_name": self.file_name,
            "timestamp": str(self.timestamp),
            "size": self.size,
            "hash": self.file_hash,
            "parent_hash": self.parent_hash,
        }

        meta_data_str = json.dumps(meta_data)

        meta_data_file_name = self.gen_meta_file_name(meta_data_str)

        with open(meta_data_file_name, "w+") as f:
            f.write(meta_data_str)

        return meta_data_file_name

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
        meta_hash = self.gen_meta_hash(meta_data_str)
        meta_data_file_name = meta_hash + ".json"
        return os.path.join(".au", meta_data_file_name)

    @staticmethod
    def gen_meta_hash(meta_data_str):
        meta_data_file_name = hashlib.sha1()
        meta_data_file_name.update(str.encode(meta_data_str))
        return meta_data_file_name.hexdigest()


def get_dataset_metadata(file_name: str) -> (str, DatasetMetaData):
    full_path = os.path.abspath(file_name)

    logging.info(f"get_metadata for file: {full_path}")

    for mdf in os.listdir(".au"):

        mdf_path = os.path.join(".au", mdf)

        try:
            mdo = DatasetMetaData(mdf_path)
            if mdo.file_name == full_path:
                return mdf_path, mdo
        except FileNotFoundError:
            continue

    return None, None
