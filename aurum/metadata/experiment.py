import os

from aurum import constants as cons
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

        parent = self.get_parent()

        if parent:
            self.parent_hash = parent.file_hash

        return super().save(destination)

    def get_parent(self):
        newest = None
        meta_data_dir = os.path.join(git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR)

        for file in os.listdir(meta_data_dir):

            full_path = os.path.join(meta_data_dir, file)

            emd = ExperimentMetaData(full_path)
            if emd.name == self.name and emd.timestamp > self.timestamp:
                newest = emd

        return newest
