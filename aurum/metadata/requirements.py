import os
import uuid

from .metadata import MetaData
from .. import constants as cons, git
from ..utils import dir_files_by_last_modification_date


class RequirementsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.contents = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        name = f"{uuid.uuid4()}.json"

        requirements_metadata_dir = \
            os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)

        destination = os.path.join(requirements_metadata_dir, name)

        return super().save(destination)


def get_latest_rmd() -> RequirementsMetaData:
    requirements_metadata_dir = \
        os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)

    files = dir_files_by_last_modification_date(requirements_metadata_dir)

    if len(files) > 0:
        return RequirementsMetaData(files[0][1])

    return RequirementsMetaData()
