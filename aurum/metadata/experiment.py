import os
from datetime import datetime

from aurum import constants as cons
from aurum import git
from aurum.metadata import MetaData
from aurum.utils import gen_file_hash


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

        if parent:
            self.parent_hash = parent.file_hash

        return super().save(destination)

    def get_parent(self):
        newest = None
        meta_data_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR)

        for file in os.listdir(meta_data_dir):

            full_path = os.path.join(meta_data_dir, file)
            if cons.KEEP_FILE not in full_path:

                emd = ExperimentMetaData(full_path)
                if emd.name == self.name and emd.timestamp > self.timestamp:
                    newest = emd

        return newest


def get_latest_experiment_metadata_by_date() -> ExperimentMetaData:

    newest = None
    now = datetime.now()

    experiment_metadata_dir = os.path.join(
        git.get_git_repo_root(),
        cons.REPOSITORY_DIR,
        cons.EXPERIMENTS_METADATA_DIR,
    )

    for file in os.listdir(experiment_metadata_dir):

        full_path = os.path.join(experiment_metadata_dir, file)

        exm = ExperimentMetaData(full_path)
        if now > exm.timestamp:
            newest = exm
            now = exm.timestamp

    return newest
