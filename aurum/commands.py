#!/usr/bin/env python3
##
## Authors: Adriano Marques
##          Nathan Martins
##          Thales Ribeiro
##
## Copyright (C) 2019 Exponential Ventures LLC
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##

__author__ = "Adriano Marques, Nathan Martins, Thales Ribeiro"
__copyright__ = "Copyright (C) 2019 Exponential Ventures LLC"
__license__ = "GNU LESSER GENERAL PUBLIC LICENSE 2.0"
__url__ = "https://github.com/exponential-ventures/aurum"
__version__ = "0.1"

import argparse

from aurum.utils import check_inside_au
from aurum.singleton import SingletonDecorator
# from aurum.base import load_parameters


@SingletonDecorator
class Parser:
    def __init__(self):
        check_inside_au()

        description = """Aurum is a new and simplified approach for data scientists to
        keep track of data and code without having to get another PhD for it. Aurum
        keeps track of all code and data changes, and lets you easily reproduce any
        experiment as well as easily compare metrics across experiments.
        """
        epilog = "And that's how you make your live easier. You're welcome."
        parser = argparse.ArgumentParser(description=description, epilog=epilog, add_help=True)

        parser.add_argument('-v', '--verbose', required=False, default=False)
        parser.add_argument('-d', '--dry-run', required=False, default=False)

        # known_params = load_parameters('parameters')
        known_params = []

        for param in known_params:
            parser.add_argument(f'-{param}', required=False)

        self.known_params, self.unknown_params = parser.parse_known_args()

        # TODO: Save preference on verbose or dry run into the instance for easy access
