import os

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.utils import gen_file_hash, dir_files_by_last_modification_date

EXPERIMENT_METADATA_DIR = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR)


class ExperimentMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.name = None
        self.dataset_hash = None
        self.code_hash = None
        self.parameter_hash = None
        self.logging_hash = None
        super().__init__(file_name)

    def save(self, destination: str) -> str:

        self.file_hash = gen_file_hash(
            os.path.join(git.get_git_repo_root(), self.file_name)
        )

        parent = self.get_parent()

        if parent.file_hash != self.file_hash:
            self.parent_hash = parent.file_hash
            return super().save(destination)

    def get_parent(self):

        files = dir_files_by_last_modification_date(EXPERIMENT_METADATA_DIR)
        if len(files) > 0:
            return ExperimentMetaData(files[0][1])

        return ExperimentMetaData()


def get_latest_experiment_metadata_by_date() -> ExperimentMetaData:
    files = dir_files_by_last_modification_date(EXPERIMENT_METADATA_DIR)
    if len(files) > 0:
        return ExperimentMetaData(files[0][1])

    return None
