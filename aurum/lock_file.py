import os


def __get_path(experiment_dir: str):
    return os.path.join(experiment_dir, ".au.lock")


def create_lock_file(experiment_dir: str, parent_branch_name: str):
    path = __get_path(experiment_dir)
    if os.path.exists(path):
        raise RuntimeError(f"Unable to lock, inside a stale experiment branch: {path}")

    with open(path, "x") as f:
        f.write(parent_branch_name)


def remove_lock_file(experiment_dir: str):
    path = __get_path(experiment_dir)

    if not os.path.exists(path):
        raise RuntimeError(f"Unable to unlock, lock file does not exist at: '{path}'")

    os.remove(path)


def get_parent_from_lock(experiment_dir: str) -> str:
    path = __get_path(experiment_dir)

    if not os.path.exists(path):
        raise RuntimeError(f"Unable to get parent, lock file does not exist at: '{path}'")

    with open(path, "r") as f:
        return f.read()
