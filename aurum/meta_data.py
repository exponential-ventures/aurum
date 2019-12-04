import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetaData:
    """
    Responsible for interacting with Meta Data files:
    - Accessing attributes such as hashes and timestamps.
    - Traverse a dataset's history.
    - Serialize and deserialize from file format.
    - Generate file hash
    - Generate meta data hash
    - Generate meta data file name
    """

    file_hash: str
    parent_hash: str
    file_name: str
    size: int
    timestamp: datetime

    def __init__(self, file_name: str = '') -> None:
        self.file_name = file_name

        if file_name != '':
            with open(file_name, 'r') as f:
                self.serialize(f.read())

    def serialize(self, raw_meta_data: str):
        so = json.loads(raw_meta_data)
        self.file_name = so.get("file_name")
        self.timestamp = so.get("timestamp")
        self.size = so.get("size")
        self.file_hash = so.get("hash")
        self.parent_hash = so.get("parent_hash")

    def deserialize(self):

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

    def gen_file_hash(self, file_name):
        sha1 = hashlib.sha1()
        buf_size = 65536  # lets read stuff in 64kb chunks!

        with open(file_name, 'rb') as f:
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