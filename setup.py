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

from setuptools import setup, find_packages

setup(
    name='aurum',
    version='0.3.0',
    description='Data and Code Versioning for Data Scientists',
    author='Adriano Marques, Nathan Martins, Thales Ribeiro',
    author_email='adriano@xnv.io, nathan@xnv.io, thales@xnv.io',
    python_requires='>=3.7.0',
    include_package_data=True,
    license="GNU LGPLv3",
    install_requires=['nvidia-ml-py3', 'psutil'],
    url='https://github.com/exponential-ventures/aurum',
    packages=find_packages(exclude=['*tests*', 'test*']),
    platforms=['any'],
    entry_points={
        'console_scripts': [
            'au = aurum:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
