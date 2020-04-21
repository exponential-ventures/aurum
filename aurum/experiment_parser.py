import argparse
import json
import os

from . import constants as cons, git
from .metadata import ParameterMetaData
from .singleton import SingletonDecorator


@SingletonDecorator
class ExperimentArgParser:
    def __init__(self):

        # TODO: Change this description so that it reflects what the ExperimentArgParser really is.
        description = """Aurum is a new and simplified approach for data scientists to
        keep track of data and code without having to get another PhD for it. Aurum
        keeps track of all code and data changes, and lets you easily reproduce any
        experiment as well as easily compare metrics across experiments.
        """
        epilog = "And that's how you make your live easier. You're welcome."

        self.known_params = None
        self.unknown_params = None

        self.parser = argparse.ArgumentParser(description=description, epilog=epilog, add_help=True)

        self.parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        self.parser.add_argument("-n", "--no-tracking", help="Don't store any metadata about this experiment",
                                 action="store_true")

        try:
            known_params = load_parameters()
        except FileNotFoundError:
            known_params = {}

        for param in known_params.keys():
            self.parser.add_argument(f'-{param}', required=False, default=known_params[param])

        self.parse_args()

        # TODO: Save preference on verbose or dry run into the instance for easy access

    def parse_args(self):
        self.known_params, self.unknown_params = self.parser.parse_known_args()


def load_parameters() -> dict:
    metadata = ParameterMetaData().get_latest()

    if metadata and metadata.file_name:
        filepath = os.path.join(
            git.get_git_repo_root(), cons.REPOSITORY_DIR, cons.PARAMETER_METADATA_DIR, metadata.file_name
        )
    else:
        filepath = None

    if filepath is not None:
        with open(filepath, 'r') as f:
            root_json = json.loads(f.read())
            return json.loads(root_json['parameters'])
    else:
        return {}
