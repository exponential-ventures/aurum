import os
import uuid

from aurum import constants as cons, git
from aurum.metadata import MetaData


class RequirementsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        super().__init__(file_name)
        self.contents = None

    def save(self, destination: str = None) -> str:
        name = f"{uuid.uuid4()}.json"
        root = git.get_git_repo_root()
        destination = os.path.join(root, cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR, name)

        return super().save(destination)


def get_latest_rmd() -> RequirementsMetaData:
    newest = RequirementsMetaData()
    requirements_metadata_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR,
                                             cons.REQUIREMENTS_METADATA_DIR)
    for file in os.listdir(requirements_metadata_dir):

        full_path = os.path.join(requirements_metadata_dir, file)

        rmd = RequirementsMetaData(full_path)
        if rmd.timestamp < newest.timestamp:
            newest = rmd

    return newest
