import logging
import subprocess

from aurum import git


def run_test_init():
    proc = subprocess.Popen(
        ["au -v init"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    _, e = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"Unable to run init. {e} {proc.returncode}")


def set_git_for_test():
    proc = git.run_git('config', '--global', 'user.email', '"test@example.com"', )
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    proc = git.run_git('config', '--global', 'user.name', '"test"', )
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(err)

    logging.debug("Git config successful")
