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


import shutil
import unittest

import aurum as au
from aurum.metadata.metrics import MetricsMetaData


class TestMetrics(unittest.TestCase):
    def setUp(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)
        au.base.run_init()

    def tearDown(self):
        for path in au.base.DEFAULT_DIRS:
            shutil.rmtree(path, ignore_errors=True)

    def test_register_metrics(self):
        au.register_metrics(resga=800, foo=2_000)
        metrics_metadata = MetricsMetaData().get_latest()
        self.assertEqual(metrics_metadata.metrics['resga'], 800)
        self.assertEqual(metrics_metadata.metrics['foo'], 2_000)
        self.assertTrue('environment' in metrics_metadata.metrics)
        self.assertTrue('hardware' in metrics_metadata.metrics)


if __name__ == '__main__':
    unittest.main()
