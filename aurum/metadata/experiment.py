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
        self.logging_hash = None
        super().__init__(file_name)

    def save(self, destination: str) -> str:

        self.file_hash = self.__hash__()

        parent = self.get_parent()

        if parent.file_hash != self.file_hash:
            self.parent_hash = parent.file_hash
            return super().save(destination)

    def get_parent(self):

        files = dir_files_by_last_modification_date(EXPERIMENT_METADATA_DIR)
        if len(files) > 0:
            return ExperimentMetaData(files[0][1])

        return ExperimentMetaData()

    def __hash__(self):
        dict_aux = self.__dict__
        del (dict_aux['experiment_id'])
        del (dict_aux['timestamp'])
        del (dict_aux['metrics_hash'])
        del (dict_aux['file_name'])
        del (dict_aux['commit_hash'])
        del (dict_aux['logging_hash'])

        return gen_dict_hash(dict_aux)


def get_latest_experiment_metadata_by_date() -> ExperimentMetaData:
    files = dir_files_by_last_modification_date(EXPERIMENT_METADATA_DIR)
    if len(files) > 0:
        return ExperimentMetaData(files[0][1])

    return None
