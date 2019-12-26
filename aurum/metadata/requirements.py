import os
import uuid

from aurum import constants as cons, git
from aurum.metadata import MetaData
from aurum.utils import dir_files_by_last_modification_date

REQUIREMENTS_METADATA_DIR = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)


class RequirementsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.contents = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        name = f"{uuid.uuid4()}.json"
        destination = os.path.join(REQUIREMENTS_METADATA_DIR, name)

        return super().save(destination)


def get_latest_rmd() -> RequirementsMetaData:
    files = dir_files_by_last_modification_date(REQUIREMENTS_METADATA_DIR)

    if len(files) > 0:
        return RequirementsMetaData(files[0][1])

    return RequirementsMetaData()
