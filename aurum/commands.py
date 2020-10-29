import argparse
import logging
import ntpath
import os
import shutil
import sys
import zipfile
from pathlib import Path

from . import constants as cons, base, git
from .dataset_tracker import check_ds_exists
from .env_builder import create_temporary_env, install_packages
from .metadata import DatasetMetaData, MetricsMetaData, ExperimentMetaData, RequirementsMetaData
from .utils import make_safe_filename, dic_to_str, copy_dir_and_files


def run_init() -> None:
    if os.path.exists(base.get_default_dirs()[0] / cons.INITIAL_COMMIT_FILE):
        logging.error("Aurum was previously initialized. Aborting.")
        sys.exit(1)

    logging.info("Initializing git...")
    git.init()

    logging.info("Creating .gitignore...")
    create_gitignore()

    logging.info("Initializing aurum...")
    au_init()

    logging.debug(f"Repository {base.get_cwd()} initialized.")


def run_add(parsed_result: argparse.Namespace, selected_dir: str) -> int:
    files_added = 0

    for f in parsed_result.files:

        # Check if file is a network address so we download it.
        # if re.search("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", f):
        #     filename = ntpath.basename(f)
        #
        #     if check_ds_exists(filename, cwd=selected_dir):
        #         logging.warning(f"Dataset {filename} already added to the system. Skipping...")
        #         continue
        #
        #     logging.info(f"Downloading {filename} from {f}")
        #     _, file_extension = os.path.splitext(f)
        #     local_path = f"{make_safe_filename(filename)}{file_extension}"
        #     download_file_from_web(f, local_path)
        #     logging.info(f"Downloaded {filename} to {local_path}")
        #     f = local_path
        # else:
        if check_ds_exists(f, cwd=selected_dir):
            logging.warning(f"Dataset {f} already added to the system. Skipping...")
            continue

        full_f = os.path.join(selected_dir, f)
        logging.debug(f"full f is {full_f}")

        if Path(git.get_git_repo_root(selected_dir)) != Path(selected_dir):
            check_file(f, cwd=git.get_git_repo_root(selected_dir))
            # Use relative from here on out.
            f = full_f.split(git.get_git_repo_root(selected_dir))[1]
        else:
            check_file(f, cwd=selected_dir)

        mdf = DatasetMetaData()
        mdf.file_name = f
        mdf.size = os.path.getsize(full_f)
        meta_data_file_name = mdf.save(cwd=git.get_git_repo_root(selected_dir))
        git.add(meta_data_file_name, cwd=git.get_git_repo_root(selected_dir))
        files_added += 1

    if files_added > 0:
        git.commit(f"Aurum added the metadata files for dataset(s) {', '.join(parsed_result.files)} to the project.",
                   cwd=selected_dir)
        print(f"\nAurum added the metadata files for the following datasets: {', '.join(parsed_result.files)}\n")
        print(f"-" * 80)
        print(f"If you'd like to add the actual dataset files to the project's repository,\n"
              f"you'll need to run the following commands:\n")

        for dataset_filename in parsed_result.files:
            print(f"git add {dataset_filename}")

        print(f"git commit -a -m 'Adding dataset files to project'\n")

    return files_added


def run_rm(parsed_result: argparse.Namespace, selected_dir: str) -> None:
    for filepath in parsed_result.files:

        filepath = check_file(filepath, cwd=git.get_git_repo_root(selected_dir))

        logging.info(f"Removing {filepath} from git")
        git.rm(filepath, soft_delete=parsed_result.soft_delete)
        logging.info(f"{filepath} removed from git")

        _, meta_data_path = DatasetMetaData().get_by_ds_name(cwd=git.get_git_repo_root(selected_dir),
                                                             file_name=filepath)

        logging.info(f"Removing meta data '{meta_data_path}' and removing from git.")

        git.rm(meta_data_path, soft_delete=parsed_result.soft_delete)

        # might have been removed by git, might not.
        if os.path.exists(meta_data_path):
            os.remove(meta_data_path)

        # remove parent dir if empty to avoid lots of empty dirs.
        parent_dir = os.path.join(selected_dir, cons.REPOSITORY_DIR, cons.DATASET_METADATA_DIR,
                                  make_safe_filename(filepath))
        if len(os.listdir(parent_dir)) <= 1:
            shutil.rmtree(parent_dir, ignore_errors=True)

        logging.info(f"Removed meta data '{meta_data_path}' and removed from git.")


def run_load(parsed_result: argparse.Namespace, skip_package_install: bool = False) -> None:
    logging.info(f"Attempting to load experiment with tag: {parsed_result.tag}")

    experiment_dir = os.path.join(cons.REPOSITORY_DIR, cons.EXPERIMENTS_METADATA_DIR)

    experiments = os.listdir(experiment_dir)
    if f"{parsed_result.tag}.json" not in experiments:
        msg = f"Unknown experiment tag: {parsed_result.tag} "
        logging.debug(msg)
        raise Exception(msg)

    emd = ExperimentMetaData(os.path.join(experiment_dir, f"{parsed_result.tag}.json"))

    requirements_metadata_dir = os.path.join(cons.REPOSITORY_DIR, cons.REQUIREMENTS_METADATA_DIR)

    for r in os.listdir(requirements_metadata_dir):
        if r == cons.KEEP_FILE:
            continue

        rmd = RequirementsMetaData(os.path.join(requirements_metadata_dir, r))
        if emd.requirements_hash == rmd.file_hash:
            git.run_git("checkout", "-B", f"{parsed_result.tag}")

            virtual_env_dir = create_temporary_env(parsed_result.tag)

            contents = list()

            for line in rmd.contents.splitlines():
                # Skip ourselves
                if "aurum" in line:
                    continue

                contents.append(line)

            if not skip_package_install:
                install_packages(virtual_env_dir, contents)

            print(f"Please activate your new virtual environment at: {virtual_env_dir}")

            if sys.platform == 'win32':
                bin_name = 'Scripts'
            else:
                bin_name = 'bin'

            full_virtual_env = os.path.join(virtual_env_dir, bin_name, "activate")

            print(f"Run 'source {full_virtual_env}'")

            break


def create_default_dirs() -> None:
    for path in base.get_default_dirs():
        if path.exists() and path.parts[-1] != cons.REPOSITORY_DIR and os.listdir(path) != ['.keep']:
            logging.error(f"Can't create {path} directory. Already exists.")
            sys.exit(1)
        logging.debug(f"Creating dir {path}")

        os.makedirs(path, exist_ok=True)
        Path(path, '.keep').touch()  # Needed to allow adding an empty directory to git


def create_gitignore() -> None:
    gitignore_path = base.get_default_dirs()[0].parent / cons.GITIGNORE_FILE
    with open(os.path.join(os.path.dirname(__file__), cons.GITIGNORE_TEMPLATE_FILE), 'rb') as template_file:
        template = template_file.read()
        with open(gitignore_path, 'ab') as gitignore:
            gitignore.write(b"\n" + template)
    git.add(gitignore_path)


def au_init() -> None:
    create_default_dirs()
    git.add_dirs(base.get_default_dirs())
    logging.info("Adding directories to git...")

    stdout, stderr = git.commit('Initial Commit')
    logging.info("Initial commit")

    initial_commit = base.get_default_dirs()[0] / cons.INITIAL_COMMIT_FILE
    open(initial_commit, 'wb').write(stdout.split()[2][:-1])
    git.add(initial_commit)
    git.commit("Recording initial commit file.")


def check_file(file_path: str, cwd: str = '') -> str:
    """
    Checks if path exists, is a file, and if absolute if can be made into a au relative path.
    If not raises SystemExit.
    """

    if cwd == '':
        cwd = git.get_git_repo_root()

    full_path = os.path.join(cwd, file_path)

    if not os.path.exists(full_path) and not os.path.exists(file_path):
        logging.error(f"Path '{file_path}' does not exist or is not in the repository: {full_path}")
        sys.exit(1)

    # if not os.path.isfile(full_path):
    #     logging.error(f"Path '{file_path}' must be a file")
    #     sys.exit(1)
    #
    # if os.path.isabs(file_path):
    #
    #     if str(base.get_cwd()) in file_path:
    #         file_path = file_path.split(str(base.get_cwd()), 1)[1][1:]
    #     else:
    #         logging.error(f"File '{file_path}' is not relative to au repository")
    #         sys.exit(1)

    return file_path


def display_metrics(experiment_ids: list) -> None:
    metrics_path = os.path.join(cons.REPOSITORY_DIR, cons.METRICS_METADATA_DIR)
    for path in os.listdir(metrics_path):
        if cons.KEEP_FILE not in path:
            metrics_metadata = MetricsMetaData(os.path.join(metrics_path, path))
            if len(experiment_ids) > 0:
                if metrics_metadata.experiment_id in experiment_ids:
                    print(dic_to_str(metrics_metadata.metrics, f'Experiment id: {metrics_metadata.experiment_id}'))
            else:
                print(dic_to_str(metrics_metadata.metrics, f'Experiment id: {metrics_metadata.experiment_id}'))


def export_experiment(parsed_args: argparse.Namespace) -> None:
    remove_dirs = []
    dataset_path = None
    repo_dir = cons.REPOSITORY_DIR
    dataset_metadata = DatasetMetaData().get_latest()
    root_path = git.get_git_repo_root()

    if dataset_metadata:

        if parsed_args.no_data:
            remove_dirs.append(os.path.join(repo_dir, dataset_metadata.file_name))
        else:
            dataset_path = dataset_metadata.file_name

    if parsed_args.no_logs:
        remove_dirs.append(os.path.join(root_path, cons.LOGS_DIR))
    if parsed_args.no_metrics:
        remove_dirs.append(os.path.join(repo_dir, cons.METRICS_METADATA_DIR))

    destiny_path = os.path.join(parsed_args.tag)
    if not Path(destiny_path).exists():
        os.makedirs(destiny_path)

    for path in base.get_default_dirs():
        if path.as_posix() in remove_dirs:
            continue
        copy_dir_and_files(path, os.path.join(destiny_path, ntpath.basename(path)))

    if dataset_path:
        copy_dir_and_files(dataset_path, os.path.join(destiny_path, ntpath.basename(dataset_path)))

    filename = os.path.join(root_path, parsed_args.tag + '.zip')
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(destiny_path):
            for file in files:
                zip_ref.write(os.path.join(root, file))

    shutil.rmtree(destiny_path, ignore_errors=True)
