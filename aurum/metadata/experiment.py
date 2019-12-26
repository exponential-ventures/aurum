import os

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.utils import gen_dict_hash, dir_files_by_last_modification_date

EXPERIMENT_METADATA_DIR = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR)


class ExperimentMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.name = None
        self.dataset_hash = None
        self.code_hash = None
        self.parameter_hash = None
        self.requirements_hash = None
        self.logging_hash = None
        super().__init__(file_name)

    def save(self, destination: str) -> str:

        self.file_hash = self.obj_hash()

        parent = self.get_parent()

        if parent.file_hash != self.file_hash:
            self.parent_hash = parent.file_hash
            return super().save(destination)

    def get_parent(self):

        files = dir_files_by_last_modification_date(EXPERIMENT_METADATA_DIR)
        if len(files) > 0:
            return ExperimentMetaData(files[0][1])

        return ExperimentMetaData()

    def obj_hash(self):
        return gen_dict_hash(
            {'code_hash': self.code_hash, 'dataset_hash': self.dataset_hash, 'parameter_hash': self.parameter_hash,
             'parent_hash': self.parent_hash, 'requirements_hash': self.requirements_hash})




def get_latest_experiment_metadata_by_date() -> ExperimentMetaData:
    files = dir_files_by_last_modification_date(EXPERIMENT_METADATA_DIR)
    if len(files) > 0:
        return ExperimentMetaData(files[0][1])

    return None
