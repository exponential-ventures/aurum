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


import sys
import logging
from tempfile import TemporaryFile

from .singleton import SingletonDecorator


class tee:
    """
    Inspired by: http://shallowsky.com/blog/programming/python-tee.html
    """

    def __init__(self, stream):
        self.temp_file = TemporaryFile(mode="w+")
        self.stream = stream

    def write(self, text):
        self.temp_file.write(text)
        self.stream.write(text)

    def flush(self):
        self.temp_file.flush()
        self.stream.flush()


@SingletonDecorator
class LoggingTracker:

    def __init__(self) -> None:
        super().__init__()

        self.stdout = tee(sys.stdout)
        self.stderr = tee(sys.stderr)
        logging.getLogger().addHandler(logging.StreamHandler(self.stdout.temp_file))

        sys.stdout = self.stdout
        sys.stderr = self.stderr
