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


import time


class Benchmark:
    def __init__(self, name: str):
        self.labels = []
        self.name = name

    def start(self):
        self.labels.append(('Start', time.time()))

    def end(self):
        self.labels.append(('End', time.time()))

    def add_label(self, name: str):
         self.labels.append((name, time.time()))

    def print(self):
        print('')
        print(self.name)
        print('')
        for label_index in range(1, len(self.labels)):
            print(
                f"{self.labels[label_index][0]} took"
                f"{self.labels[label_index][1] - self.labels[label_index - 1][1]: .3f} seconds")
        print('')

