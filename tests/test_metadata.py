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


import unittest
from datetime import datetime

from aurum.metadata import MetaData


class MetaDataTestCase(unittest.TestCase):

    def test_serialize(self):
        md = MetaData()
        md.timestamp = datetime(2019, 12, 5, 15, 30)
        md.name = "test"
        raw_json = md.serialize()
        self.assertEqual(
            raw_json,
            f'{{"parent_hash": null, "file_hash": null, "cwd": "/tmp/repository", "file_name": "", "timestamp": 1575559800.0, '
            f'"experiment_id": "{md.experiment_id}", "name": "test"}}'
        )

    def test_save(self):
        md = MetaData()
        md.timestamp = datetime(2019, 12, 5, 15, 30)
        md.name = "test"
        md.save("/tmp/a.json")
        with open("/tmp/a.json", 'r') as r:
            self.assertEqual(
                r.read(),
                f'{{"parent_hash": null, "file_hash": null, "cwd": "/tmp/repository", "file_name": "", "timestamp": 1575559800.0, '
                f'"experiment_id": "{md.experiment_id}", "name": "test"}}'
            )


if __name__ == '__main__':
    unittest.main()
