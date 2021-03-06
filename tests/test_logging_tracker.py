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


import logging
import sys
import unittest

from aurum.logging_tracker import LoggingTracker


class LoggingTrackerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        if hasattr(LoggingTracker, "instance"):
            LoggingTracker.instance = None

    def test_stdout(self):
        lt = LoggingTracker()
        print("hello world")
        lt.stdout.temp_file.seek(0)
        c = lt.stdout.temp_file.read()
        self.assertEqual(c, "hello world\n")

    def test_stderr(self):
        lt = LoggingTracker()
        print("hello world", file=sys.stderr)
        lt.stderr.temp_file.seek(0)
        c = lt.stderr.temp_file.read()
        self.assertEqual(c, "hello world\n")

    def test_logging_stdout(self):
        lt = LoggingTracker()
        logging.critical("hello world")
        lt.stdout.temp_file.seek(0)
        c = lt.stdout.temp_file.read()
        self.assertEqual(c, "hello world\n")


if __name__ == '__main__':
    unittest.main()
