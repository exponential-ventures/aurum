import os
import uuid
from datetime import datetime

from aurum import constants as cons, git
from aurum.metadata import MetaData


class RequirementsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.file_hash = None
        self.parent_hash = None
        self.contents = None
        self.timestamp = datetime.now()

        if file_name != '':
            with open(file_name, 'r') as f:
                self.deserialize(f.read())

    def save(self, destination: str = None) -> str:
        name = f"{uuid.uuid4()}.json"
        root = git.get_git_repo_root()
        destination = os.path.join(root, cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR, name)

        return super().save(destination)

    def deserialize(self, raw_json: str):
        super().deserialize(raw_json)
        self.timestamp = datetime.fromtimestamp(self.timestamp)


def get_latest_rmd() -> RequirementsMetaData:
    newest = RequirementsMetaData()
    root = git.get_git_repo_root()

    for rmf_path in os.listdir(os.path.join(root, cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)):

        full_rmf_path = os.path.join(root, cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR, rmf_path)

        rmf = RequirementsMetaData(full_rmf_path)
        if rmf.timestamp < newest.timestamp:
            newest = rmf

    return newest
