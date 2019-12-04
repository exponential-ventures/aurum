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

from setuptools import find_packages, setup

setup(
    name='aurum',
    version='0.1',
    description='Aurum is a new and simplified approach for data scientists to keep track of data and code without having to get another PhD for it.',
    author='Adriano Marques, Nathan Martins, Thales Ribeiro',
    author_email='adriano@xnv.io, nathan@xnv.io, thales@xnv.io',
    python_requires='>=3.7.0',
    install_requires=[],
    scripts=['aurum/au'],
    include_package_data=True,
    url='https://github.com/exponential-ventures/aurum',
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
