import os

from .metadata import MetaData
from .. import constants as cons, git


class RequirementsMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.contents = None
        super().__init__(file_name)

    def save(self, destination: str = None) -> str:
        name = f"{self.file_hash}.json"

        destination = os.path.join(self.get_dir(), name)

        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            cons.REPOSITORY_DIR,
            cons.REQUIREMENTS_METADATA_DIR,
        )
