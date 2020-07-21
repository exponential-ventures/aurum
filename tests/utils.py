import subprocess

from aurum import git


def run_test_init(selected_dir: str):
    proc = subprocess.run(
        ["au --verbose init"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=selected_dir,
    )

    if proc.returncode != 0:
        raise RuntimeError(f"Unable to run init.{proc.stderr} {proc.returncode}")


def set_git_for_test(selected_dir: str):

    proc = git.run_git('init', cwd=selected_dir)
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    proc = git.run_git('config', 'user.email', '"test@example.com"', cwd=selected_dir)
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    proc = git.run_git('config', 'user.name', '"test"', cwd=selected_dir)
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)
