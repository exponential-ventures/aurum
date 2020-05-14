import hashlib
import logging
import subprocess

from .metadata import RequirementsMetaData


def is_new_requirements() -> (bool, str):
    """
    Run a pip freeze and create a hash to be saved in the requirements metadata, remember that we will also need to
    record the parent requirements (latest by date, if it exists) as well as all the contents of the pip freeze list
    in a alphabetically sorted list.

    Make sure that the metadata is a linked list and can be easily browsed to find the parent even if you don't know
    who the parent is (similar to all other metadata implemented in the system).

    If there is a change in the results from freeze, this module should indicate that this is a new experiment, and
    create the metadata to document this. If there is no previous metadata (experiment is being run for the first time)
    then the code should proceed as if this is a brand new experiment, except that parent will be None.
    """

    process = subprocess.run("pip freeze", shell=True, check=True, capture_output=True)
    output = process.stdout
    logging.debug("\n" + ("-"*80) + f"\nInstalled packages:\n\n{output.decode('utf-8')}" + ("-" *80) + "\n")
    packages_hash = hashlib.sha1()
    packages_hash.update(output)
    packages_hash = packages_hash.hexdigest()

    latest_mdf = RequirementsMetaData().get_latest()

    if not latest_mdf:
        logging.debug("This is a new requirements")
        rmd = RequirementsMetaData()
        rmd.file_hash = packages_hash
        rmd.contents = output.decode()
        rmd.save()
        return True, rmd.file_hash

    elif latest_mdf and latest_mdf.file_hash != packages_hash:
        logging.debug("This are changed requirements")
        rmd = RequirementsMetaData()
        rmd.file_hash = packages_hash
        rmd.parent_hash = latest_mdf.file_hash
        rmd.contents = output.decode()
        rmd.save()
        return True, rmd.file_hash

    return False, ""
