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

import sys
import argparse

from aurum.base import execute_commands

# params = ['a', 'b', 'batch_size']

def parameters(**kwargs):
    # setattr(sys.modules[__name__], 'params', list(kwargs.keys()))
    parse_params = main(list(kwargs.keys()))
    for key in kwargs.keys():
        value = None
        try:
            if key in parse_params:
                value = parse_params.__getattribute__(key)
        except:
            pass

        setattr(sys.modules[__name__], key, value or kwargs[key])

def main(params):
    description = """Aurum is a new and simplified approach for data scientists to
    keep track of data and code without having to get another PhD for it. Aurum
    keeps track of all code and data changes, and lets you easily reproduce any
    experiment as well as easily compare metrics across experiments.
    """
    epilog = "And that's how you make your live easier. You're welcome."
    parser = argparse.ArgumentParser(description=description, epilog=epilog, add_help=True)

    for param in params:
        parser.add_argument(f'-{param}', required=False)

    # setattr(sys.modules[__name__], 'parse_params',  parser.parse_args())
    return parser.parse_args()

if __name__ == "__main__":
    main()

# main()
