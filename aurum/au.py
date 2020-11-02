#!/usr/bin/env python3
#
# Authors: Adriano Marques
#          Nathan Martins
#          Thales Ribeiro
#
# Copyright (C) 2019 Exponential Ventures LLC
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Library General Public
#    License as published by the Free Software Foundation; either
#    version 2 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Library General Public License for more details.
#
#    You should have received a copy of the GNU Library General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

import argparse

import pkg_resources

import aurum.constants as cons
from aurum.base import execute_commands

__author__ = "Adriano Marques, Nathan Martins, Thales Ribeiro"
__copyright__ = "Copyright (C) 2019 Exponential Ventures LLC"
__license__ = "GNU LESSER GENERAL PUBLIC LICENSE 2.0"
__url__ = "https://github.com/exponential-ventures/aurum"
__version__ = pkg_resources.require("aurum")[0].version


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
    parser_init = subparsers.add_parser(cons.INIT, help="initialize current directory as an aurum repository")
    parser_init.set_defaults(subcommand=cons.INIT)

    #######
    # load
    parser_load = subparsers.add_parser("load", help="load a specific experiment by tag")
    parser_load.set_defaults(subcommand="load")
    parser_load.add_argument("tag", type=str, action="store")

    #######
    # data
    parser_data = subparsers.add_parser(cons.DATA, help="operations on data files")
    parser_data.set_defaults(subcommand=cons.DATA)

    subparser_data = parser_data.add_subparsers()

    parser_data_add = subparser_data.add_parser(cons.DATA_ADD, help="add specified data file(s) to the data index")
    parser_data_add.set_defaults(subcommand2=cons.DATA_ADD)
    parser_data_add.add_argument("files", type=str, nargs='+')

    ######
    # add
    parser_add = subparsers.add_parser(cons.DATA_ADD, help="add specified file to the index")
    parser_add.set_defaults(subcommand=cons.DATA_ADD)

    subparser_add = parser_add.add_subparsers()

    parser_add_files = subparser_add.add_parser(cons.DATA_ADD, help="add specified file(s) to the data index")
    parser_add_files.set_defaults(subcommand2=cons.DATA_ADD)
    parser_add_files.add_argument("files", type=str, nargs="+")

    #######
    # data rm
    parser_data_rm = subparser_data.add_parser(cons.DATA_RM, help="remove specified data file(s) from the data index")
    parser_data_rm.set_defaults(subcommand2=cons.DATA_RM)
    parser_data_rm.add_argument("files", type=str, nargs="+")

    deletion_type_parser = parser_data_rm.add_mutually_exclusive_group(required=False)
    deletion_type_parser.add_argument("--soft-delete", dest="soft_delete", action="store_true")
    deletion_type_parser.add_argument("--hard-delete", dest="soft_delete", action="store_false")
    parser_data_rm.set_defaults(soft_delete=True)

    #######
    # metrics
    parser_metrics = subparsers.add_parser(cons.METRICS, help="display metrics")
    parser_metrics.set_defaults(subcommand=cons.METRICS)
    parser_metrics.add_argument(cons.EXPERIMENT_IDS, type=str, nargs='?', default=None)

    #######
    # export tag
    parser_export = subparsers.add_parser(cons.EXPORT_TAG, help="export tag")
    parser_export.set_defaults(subcommand=cons.EXPORT_TAG)
    parser_export.add_argument("tag", type=str, action="store")
    parser_export.add_argument("--no-data", dest="no_data", action="store_true", default=False)
    parser_export.add_argument("--no-metrics", dest="no_metrics", action="store_true", default=False)
    parser_export.add_argument("--no-logs", dest="no_logs", action="store_true", default=False)

    ######
    # Other arguments
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    return parser


def main() -> None:
    execute_commands(config_parser())


if __name__ == "__main__":
    main()
