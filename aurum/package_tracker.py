import hashlib
import logging
import subprocess


def installed_packages_hash() -> str:
    process = subprocess.run("pip freeze", shell=True, check=True, capture_output=True)
    output = process.stdout
    packages_hash = hashlib.sha1()
    logging.debug(f"\nInstalled packages: \n {output} \n\n")
    packages_hash.update(output)
    return packages_hash.hexdigest()



















