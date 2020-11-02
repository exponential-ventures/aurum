import argparse
import logging
import os
import platform
import sys
from pathlib import Path

import psutil
from pynvml import (
    nvmlInit,
    nvmlDeviceGetCount,
    nvmlSystemGetDriverVersion,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
    nvmlShutdown,
    NVMLError,
)

from . import constants as cons, git
from .commands import (
    run_init,
    run_rm,
    run_add,
    run_load,
    display_metrics,
    export_experiment,
)
from .lock_file import remove_lock_file, get_parent_from_lock
from .metadata import (
    ParameterMetaData,
    WeightsMetaData,
    MetricsMetaData,
    ExperimentMetaData,
    DatasetMetaData,
    CodeMetaData,
    RequirementsMetaData,
)
from .theorem import Theorem
from .time_tracker import time_tracker
from .utils import size_in_gb, dic_to_str


def get_cwd():
    return Path(os.getcwd())


def get_default_dirs():
    return [
        get_cwd() / cons.REPOSITORY_DIR,
        get_cwd() / "src",
        get_cwd() / "logs",
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.METRICS_METADATA_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.WEIGHTS_METADATA_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.WEIGHTS_METADATA_DIR, cons.WEIGHTS_BINARIES_DIR),
        get_cwd() / os.path.join(cons.REPOSITORY_DIR, cons.CODE_METADATA_DIR)
    ]


def execute_commands(parser: argparse.ArgumentParser) -> None:
    parsed = parser.parse_args()

    logging.getLogger().setLevel(logging.DEBUG if parsed.verbose else logging.WARNING)

    logging.debug(f"Parser arguments: {parsed}")

    git.check_git()

    if os.getcwd().startswith(cons.REPOSITORY_DIR):
        parser.error(f"Cannot run commands from inside '.au' folder")

    if not hasattr(parsed, "subcommand"):
        parser.error(f"No command was passed in")

    if parsed.subcommand == cons.INIT:
        run_init()
    elif parsed.subcommand == cons.LOAD:
        data_command_checker(parser)
        run_load(parsed)
    elif parsed.subcommand == cons.DATA:

        if hasattr(parsed, "subcommand2") and parsed.subcommand2 == cons.DATA_RM:
            data_command_checker(parser)
            run_rm(parsed, selected_dir=get_cwd())
        if hasattr(parsed, "subcommand2") and parsed.subcommand2 == cons.DATA_ADD:
            data_command_checker(parser)
            run_add(parsed, selected_dir=get_cwd())
        else:
            parser.error("Unknown command for data")
    elif parsed.subcommand == cons.METRICS:
        experiment_ids = []
        if parsed.experiment_ids:
            experiment_ids = parsed.experiment_ids.split(',')
        display_metrics(experiment_ids)
    elif parsed.subcommand == cons.EXPORT_TAG:
        data_command_checker(parser)
        if parsed.tag not in git.current_branch_name():
            run_load(parsed, skip_package_install=True)
        export_experiment(parsed)


def data_command_checker(parser: argparse.ArgumentParser):
    if not git.running_from_git_repo():
        parser.error(f"You are not running from inside a au repository")

    repo_root = git.get_git_repo_root()

    if not os.path.exists(os.path.join(repo_root, cons.REPOSITORY_DIR)):
        parser.error(f"Path '.au' does not exist, please run au init")


def parameters(cwd: str = '', **kwargs):
    if cwd == '':
        cwd = get_cwd()

    from .experiment_parser import ExperimentArgParser

    p = ExperimentArgParser()

    for param, default in kwargs.items():
        if param not in p.known_params:
            p.parser.add_argument(f'-{param}', required=False, default=default)

    parsed_args = p.parser.parse_args()

    # Give people the option to avoid parameter checking.
    if 'unsafe_parameter_checking' in kwargs.keys():
        unsafe_parameter_checking = kwargs['unsafe_parameter_checking']
    elif p.known_params.unsafe_parameter_checking:
        unsafe_parameter_checking = True
    else:
        unsafe_parameter_checking = False

    if len(p.unknown_params) > 0 and not unsafe_parameter_checking:
        raise RuntimeError(f"Unknown parameters passed to experiment: {' '.join(p.unknown_params)} || {parsed_args}")

    new_dict = {**kwargs, **p.known_params.__dict__}

    for key in new_dict.keys():
        setattr(sys.modules['aurum'], key, new_dict[key])

    pmd = ParameterMetaData()
    pmd.parameters = new_dict

    latest_exp = ExperimentMetaData().get_latest(
        subdir_path=os.path.join(cwd, cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR)
    )

    if (latest_exp and latest_exp.parameter_hash != pmd.parameter_hash) or (latest_exp is None):
        Theorem().parameters_did_change(pmd.parameter_hash)
        meta_data_file_name = pmd.save(cwd=cwd)
        git_proc = git.run_git("add", meta_data_file_name)

        result = git_proc.wait()
        if result != 0:
            message = f"Unable to run 'git add {meta_data_file_name}' Exit code: {result}\n"
            if git_proc.stderr:
                message += f"{git_proc.stderr.read()}\n"
            logging.error(message)


def register_metrics(cwd: str = '', **kwargs):
    if cwd == '':
        cwd = get_cwd()

    swap_mem = psutil.swap_memory()
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')

    hardware_metric = {'environment': {'python_version': platform.python_version()},
                       'run time': str(time_tracker.log_time()),
                       'run time in seconds': time_tracker.log_time().total_seconds(),
                       'hardware': {
                           'swap_memory': {
                               'total': size_in_gb(swap_mem.total)
                           },
                           'virtual_memory': {
                               'total': size_in_gb(virtual_memory.total)
                           },
                           'cpu': {
                               'physical_cores': psutil.cpu_count(logical=False),
                               'total_cores': psutil.cpu_count(),
                               'frequency': psutil.cpu_freq().current,
                           },
                           'disk': {
                               'total': size_in_gb(disk_usage.total),
                           },
                           'gpu(s)': gpu_info()
                       }

                       }

    metrics = {**kwargs, **hardware_metric}
    save_metrics(cwd=cwd, **metrics)


def gpu_info() -> dict:
    info = dict()

    try:
        nvmlInit()
    except NVMLError:
        info['no-gpu'] = 'No Nvidia GPU detected'
        return info

    device_count = nvmlDeviceGetCount()

    info['driver_version'] = nvmlSystemGetDriverVersion().decode()
    info['device_count'] = device_count
    info['device'] = dict()
    for i in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        memory = nvmlDeviceGetMemoryInfo(handle)

        info['device'][i] = dict()
        info['device'][i]['name'] = str(nvmlDeviceGetName(handle))

        info['device'][i]['memory'] = dict()

        info['device'][i]['memory']['total'] = str(size_in_gb(memory.total))

    nvmlShutdown()

    return info


def save_metrics(cwd: str, **kwargs):
    mmd = MetricsMetaData()
    mmd.metrics = kwargs

    meta_data_file_name = mmd.save(cwd=cwd)

    if meta_data_file_name:

        git_proc = git.run_git("add", meta_data_file_name)

        result = git_proc.wait()
        if result != 0:
            message = f"Unable to run 'git add {meta_data_file_name}' Exit code: {result}\n"
            if git_proc.stderr:
                message += f"{git_proc.stderr.read()}\n"
            logging.error(message)


def save_weights(model_encoded, cwd: str = "", ):
    meta_data_file_name = None
    wmd = WeightsMetaData()
    if cwd == "":
        cwd = get_cwd()

    if Theorem().has_any_change():
        wmd.save_binary(model_encoded)
        meta_data_file_name = wmd.save(cwd)

    if meta_data_file_name:

        git_proc = git.run_git("add", meta_data_file_name)

        result = git_proc.wait()
        if result != 0:
            message = f"Unable to run 'git add {meta_data_file_name}' Exit code: {result}\n"
            if git_proc.stderr:
                message += f"{git_proc.stderr.read()}\n"
            logging.error(message)


def load_weights(cwd: str = ""):
    if cwd == "":
        cwd = get_cwd()

    wmd = WeightsMetaData().get_latest(subdir_path=os.path.join(cwd, cons.REPOSITORY_DIR, cons.WEIGHTS_METADATA_DIR))

    return wmd.load_binary()


def end_experiment() -> bool:
    commit_msg = ""

    theorem = Theorem()
    if theorem.has_any_change():

        mdt = ExperimentMetaData()

        mdt.file_name = theorem.experiment_id
        metrics_metadata = MetricsMetaData().get_latest() or MetricsMetaData()
        weights_metadata = WeightsMetaData().get_latest() or WeightsMetaData()
        parameters_metadata = ParameterMetaData().get_latest() or ParameterMetaData()
        requirements_metadata = RequirementsMetaData().get_latest() or RequirementsMetaData()
        dataset_metadata = DatasetMetaData().get_latest() or DatasetMetaData()
        code_metadata = CodeMetaData().get_latest() or CodeMetaData()
        destination = os.path.join(cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR, f"{theorem.experiment_id}.json")

        mdt.metrics_hash = metrics_metadata.file_hash
        mdt.weights_hash = weights_metadata.file_hash
        mdt.parameter_hash = parameters_metadata.file_hash
        mdt.requirements_hash = requirements_metadata.file_hash
        mdt.code_hash = code_metadata.file_hash
        mdt.dataset_hash = dataset_metadata.file_hash

        if metrics_metadata.metrics:
            commit_msg += dic_to_str(metrics_metadata.metrics, 'Metrics')

        if parameters_metadata.parameters:
            commit_msg += dic_to_str(parameters_metadata.parameters, 'Parameters')

        if weights_metadata.file_hash:
            commit_msg += f"\n Weights hash: {weights_metadata.file_hash}"

        if requirements_metadata.file_hash:
            commit_msg += f"\n Requirements hash {requirements_metadata.file_hash}"

        if dataset_metadata.file_hash:
            commit_msg += f"\n Dataset hash: {dataset_metadata.file_hash}"
        else:
            logging.warning("No dataset detected. Please, run 'au data add' or 'au.use_dataset")

        if code_metadata.file_hash:
            commit_msg += f"\n Code hash: {code_metadata.file_hash}"
        else:
            logging.warning("Please, add the source-code under the 'src' folder")

        mdt.commit_hash = git.last_commit_hash()
        mdt.save(destination)

        # Parent branch
        parent_branch = get_parent_from_lock(os.getcwd())

        # Remove lock
        remove_lock_file(os.getcwd())

        # Commit and push branch once the experiment is ended
        git.add_dirs(get_default_dirs())
        git.commit(f"Experiment ID {theorem.experiment_id}", commit_msg)
        git.tag(theorem.experiment_id, commit_msg)

        # git push all branches
        git.push()

        # git push all tags
        git.push_tags()

        # Return to parent and
        git.checkout_branch(parent_branch)

        # Delete local experiment branch
        # current_branch = git.current_branch_name()
        # git.delete_branch(current_branch)

        return True

    return False
