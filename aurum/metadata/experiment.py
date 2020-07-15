import os

from .metadata import MetaData
from .. import constants as cons
from .. import git
from ..utils import gen_dict_hash


class ExperimentMetaData(MetaData):

    def __init__(self, file_name: str = '') -> None:
        self.name = None
        self.dataset_hash = None
        self.code_hash = None
        self.parameter_hash = None
        self.requirements_hash = None
        self.logging_hash = None
        self.weights_hash = None
        super().__init__(file_name)

    def save(self, destination: str) -> str:
        self.file_hash = self.obj_hash()

        parent = self.get_latest()

        if parent and parent.file_hash != self.file_hash:
            self.parent_hash = parent.file_hash

        return super().save(destination)

    def get_dir(self):
        return os.path.join(
            git.get_git_repo_root(),
            cons.REPOSITORY_DIR,
            cons.EXPERIMENTS_METADATA_DIR,
        )

    def obj_hash(self):
        return gen_dict_hash(
            {
                'code_hash': self.code_hash,
                'dataset_hash': self.dataset_hash,
                'parameter_hash': self.parameter_hash,
                'parent_hash': self.parent_hash,
                'requirements_hash': self.requirements_hash,
            }
        )
