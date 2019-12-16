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

from aurum.logging_tracker import LoggingTracker

from aurum import execute_commands


def config_parser() -> argparse.ArgumentParser:
    description = """Aurum is a new and simplified approach for data scientists to
    keep track of data and code without having to get another PhD for it. Aurum
    keeps track of all code and data changes, and lets you easily reproduce any
    experiment as well as easily compare metrics across experiments.
    """
    epilog = "And that's how you make your live easier. You're welcome."
    parser = argparse.ArgumentParser(description=description, epilog=epilog, add_help=True)

    subparsers = parser.add_subparsers()

    #######
    # init
    parser_init = subparsers.add_parser("init", help="initialize current directory as an aurum repository")
    parser_init.set_defaults(subcommand="init")

    #######
    # data
    parser_data = subparsers.add_parser("data", help="operations on data files")
    parser_data.set_defaults(subcommand="data")

    subparser_data = parser_data.add_subparsers()

    parser_data_add = subparser_data.add_parser("add", help="add specified data file(s) to the data index")
    parser_data_add.set_defaults(subcommand2="add")
    parser_data_add.add_argument("files", type=str, nargs='+')

    ######
    # add
    parser_add = subparsers.add_parser("add", help="add specified file to the index")
    parser_add.set_defaults(subcommand="add")

    subparser_add = parser_add.add_subparsers()

    parser_add_files = subparser_add.add_parser("add", help="add specified file(s) to the data index")
    parser_add_files.set_defaults(subcommand2="add")
    parser_add_files.add_argument("files", type=str, nargs="+")

    #######
    # data rm
    parser_data_rm = subparser_data.add_parser("rm", help="remove specified data file(s) from the data index")
    parser_data_rm.set_defaults(subcommand2="rm")
    parser_data_rm.add_argument("files", type=str, nargs="+")

    deletion_type_parser = parser_data_rm.add_mutually_exclusive_group(required=False)
    deletion_type_parser.add_argument("--soft-delete", dest="soft_delete", action="store_true")
    deletion_type_parser.add_argument("--hard-delete", dest="soft_delete", action="store_false")
    parser_data_rm.set_defaults(soft_delete=True)

    ######
    # Other arguments
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    return parser


def main() -> None:
    execute_commands(config_parser())


if __name__ == "__main__":
    main()
else:
    lt = LoggingTracker()
