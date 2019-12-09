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

import platform
import psutil
from aurum.base import execute_commands


def register_metrics(**kwargs):
    swap_mem = psutil.swap_memory()
    virtual_memory = psutil.virtual_memory()

    hardware_metric = {'pythton_version': platform.python_version(),
      'swap_memory': {
          'total': swap_mem.total,
          'used': swap_mem.used,
          'free': swap_mem.free
      },
      'virtual_memory': {
          'total': size_in_gb(virtual_memory.total),
          'free': size_in_gb(virtual_memory.free),
          'used': virtual_memory.used,
          'used_percent': virtual_memory.percent
      },
      'cpu': {
        'physical_cores': psutil.cpu_count(logical=False),
        'total_cores': psutil.cpu_count(),
        'frequency': psutil.cpu_freq().current,
      }

    }

    metrics = {**hardware_metric, **kwargs}
    print(metrics)


def size_in_gb(size):
    return size / float(1 << 30)
