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

from aurum.au import main
from aurum.base import execute_commands, save_parameters, parameters, register_metrics, save_metrics
from aurum.dry_run import Dehydrator
from aurum.experiment_parser import ExperimentArgParser
from aurum.logging_tracker import LoggingTracker
from aurum.theorem import Theorem
from aurum.time_tracker import time_tracker

parser = ExperimentArgParser()

if parser.known_params.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

if parser.known_params.dry_run:
    Dehydrator().on()

LoggingTracker()

__all__ = [execute_commands, save_parameters, parameters, register_metrics]
