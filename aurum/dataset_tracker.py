import hashlib
import os

from .metadata import DatasetMetaData, ExperimentMetaData
from .singleton import SingletonDecorator
from .theorem import Theorem


@SingletonDecorator
class DatasetTracker:

    def __init__(self) -> None:
        super().__init__()
        self.datasets = list()

    def dataset_hash(self, cwd: str):
        full_hash_str = ""

        for ds in self.datasets:
            dsm, _ = DatasetMetaData().get_by_ds_name(ds, cwd=cwd)
            full_hash_str += dsm.file_hash

        full_hash = hashlib.sha1()
        full_hash.update(full_hash_str.encode())
        return full_hash.hexdigest()


def use_datasets(*args, cwd: str = '', ):
    if cwd == '':
        cwd = os.getcwd()

    dt = DatasetTracker()

    for ds in args:
        if not check_ds_exists(ds):
            raise Exception(
                f"Dataset '{ds}' not found. Please make sure it has been added via 'au data add dataset_name'"
            )

    for ds in args:
        dt.datasets.append(ds)

    is_new, str_hash = is_new_dataset(cwd)

    if is_new:
        Theorem().dataset_did_change(str_hash)


def check_ds_exists(file_name: str, cwd: str = '') -> bool:
    try:
        dmd = DatasetMetaData()
        if cwd != '':
            dmd.cwd = cwd
        dmd.get_by_ds_name(file_name=file_name, cwd=cwd)
        return True
    except FileNotFoundError:
        return False


def is_new_dataset(cwd: str) -> (bool, str):
    last_experiment_run = ExperimentMetaData().get_latest()
    currently_using = DatasetTracker().dataset_hash(cwd)

    if last_experiment_run is None:
        return True, currently_using
    elif last_experiment_run and last_experiment_run.dataset_hash != currently_using:
        return True, currently_using

    return False, ""
