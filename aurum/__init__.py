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
import platform
import psutil
from pynvml import *

from aurum.base import execute_commands, save_parameters, parameters
from aurum.metadata import load_parameters
from aurum.au import main
from aurum.commands import Parser
from aurum.base import execute_commands, save_metrics
from aurum.utils import size_in_gb


def register_metrics(**kwargs):
    swap_mem = psutil.swap_memory()
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')

    hardware_metric = {'environment': {'python_version': platform.python_version()},
                       'hardware': {
                           'swap_memory': {
                               'total': size_in_gb(swap_mem.total),
                               'used': size_in_gb(swap_mem.used),
                               'free': size_in_gb(swap_mem.free)
                           },
                           'virtual_memory': {
                               'total': size_in_gb(virtual_memory.total),
                               'free': size_in_gb(virtual_memory.free),
                               'used': size_in_gb(virtual_memory.used),
                               'used_percent': virtual_memory.percent
                           },
                           'cpu': {
                               'physical_cores': psutil.cpu_count(logical=False),
                               'total_cores': psutil.cpu_count(),
                               'frequency': psutil.cpu_freq().current,
                           },
                           'disk_usage': {
                               'total': size_in_gb(disk_usage.total),
                               'used': size_in_gb(disk_usage.used),
                               'free': size_in_gb(disk_usage.free),
                               'used_percent': disk_usage.percent
                           },
                           'gpu(s)': gpu_info()
                       }

                       }

    metrics = {**kwargs, **hardware_metric}
    # save_metrics('metrics', **metrics)
    print(metrics)


def gpu_info():
    info = {}
    try:
        nvmlInit()
    except:
        info['no-gpu'] = 'No Nvidia GPU detected'
        return info

    device_count = nvmlDeviceGetCount()

    info['driver_version'] = nvmlSystemGetDriverVersion().decode()
    info['device_count'] = device_count
    info['device'] = {}
    for i in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        memory = nvmlDeviceGetMemoryInfo(handle)
        info['device'][i] = nvmlDeviceGetName(handle)
        info['device'][i]['memory']['total'] = size_in_gb(memory.total)
        info['device'][i]['memory']['free'] = size_in_gb(memory.free)
        info['device'][i]['memory']['used'] = size_in_gb(memory.used)

    nvmlShutdown()

    return info


parser = Parser()

if parser.known_params.verbose:
    logging.setLevel(logging.DEBUG)

__all__ = [execute_commands, save_parameters, load_parameters, parameters]
