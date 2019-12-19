import subprocess


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
