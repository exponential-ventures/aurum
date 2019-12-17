import argparse

from aurum.metadata import load_parameters
from aurum.singleton import SingletonDecorator
from aurum.utils import check_inside_au


@SingletonDecorator
class Parser:
    def __init__(self):
        # check_inside_au()

        description = """Aurum is a new and simplified approach for data scientists to
        keep track of data and code without having to get another PhD for it. Aurum
        keeps track of all code and data changes, and lets you easily reproduce any
        experiment as well as easily compare metrics across experiments.
        """
        epilog = "And that's how you make your live easier. You're welcome."
        self.parser = argparse.ArgumentParser(description=description, epilog=epilog, add_help=True)

        self.parser.add_argument('-v', '--verbose', required=False, default=False)
        self.parser.add_argument('-d', '--dry-run', required=False, default=False)

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
