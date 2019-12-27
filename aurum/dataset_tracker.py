import hashlib
from aurum.theorem import Theorem
from .metadata.dataset import get_dataset_metadata
from .metadata.experiment import get_latest_experiment_metadata_by_date
from .singleton import SingletonDecorator


@SingletonDecorator
class DatasetTracker:

    def __init__(self) -> None:
        super().__init__()
        self.datasets = list()

    def dataset_hash(self):
        full_hash_str = ""

        for ds in self.datasets:
            _, dsm = get_dataset_metadata(ds)
            full_hash_str += dsm.file_hash

        full_hash = hashlib.sha1()
        full_hash.update(full_hash_str.encode())
        return full_hash.hexdigest()


def use_datasets(*args):
    dt = DatasetTracker()

    for ds in args:
        if not check_ds_exists(ds):
            raise Exception(
                f"Dataset '{ds}' not found. Please make sure it has been added via 'au data add dataset_name'"
            )
    for ds in args:
        dt.datasets.append(ds)

    is_new, str_hash = is_new_dataset()

    if is_new():
        Theorem().dataset_did_change(str_hash)


def check_ds_exists(file_name: str) -> bool:
    try:
        get_dataset_metadata(file_name)
        return True
    except FileNotFoundError:
        return False


def is_new_dataset() -> (bool, str):
    last_experiment_run = get_latest_experiment_metadata_by_date()
    currently_using = DatasetTracker().dataset_hash()

    if last_experiment_run is None:
        return True, currently_using
    elif last_experiment_run and last_experiment_run.dataset_hash != currently_using:
        return True, currently_using

    return False, ""
