import os

from aurum import git
from aurum.metadata import MetaData
from aurum.utils import gen_file_hash


class ExperimentMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        super().__init__(file_name)
        self.name = None
        self.dataset_hash = None
        self.code_hash = None
        self.parameter_hash = None
        self.logging_hash = None

    def save(self, destination: str) -> str:
        self.file_hash = gen_file_hash(
            os.path.join(git.get_git_repo_root(), self.file_name)
        )
        return super().save(destination)
