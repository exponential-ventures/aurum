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

import logging
import os
import sys
from pathlib import PurePosixPath, PureWindowsPath

from .au import main
from .base import execute_commands, parameters, register_metrics, save_metrics, end_experiment
from .dataset_tracker import use_datasets
from .dry_run import Dehydrator
from .experiment_parser import ExperimentArgParser
from .logging_tracker import LoggingTracker
from .package_tracker import is_new_requirements
from .theorem import Theorem
from .time_tracker import time_tracker
from .utils import check_inside_au

# TODO: Check if this works on windows.
if os.name == 'nt':
    command = PureWindowsPath(sys.argv[0]).name
else:
    command = PurePosixPath(sys.argv[0]).name

if command is not 'au' and 'unittest' not in command:

    check_inside_au()
    parser = ExperimentArgParser()

    if parser.known_params.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if parser.known_params.no_tracking is True:
        Dehydrator().on()

    LoggingTracker()

    requirements_changed, r_hash = is_new_requirements()
    if requirements_changed:
        Theorem().requirements_did_change(r_hash)

__all__ = [
    execute_commands,
    parameters,
    register_metrics,
    use_datasets,
    end_experiment
]
