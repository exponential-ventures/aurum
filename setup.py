#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## ----------------
## |              |
## | CONFIDENTIAL |
## |              |
## ----------------
##
## Copyright Exponential Ventures LLC (C), 2019 All Rights Reserved
##
## Author: Thales Ribeiro <thales@xnv.io>
##
## If you do not have a written authorization to read this code
## PERMANENTLY REMOVE IT FROM YOUR SYSTEM IMMEDIATELY.
##

from setuptools import setup, find_packages

setup(
    name='aurum',
    version='0.1.2',
    description='Data and Code Versioning for Data Scientists',
    author='Adriano Marques, Nathan Martins, Thales Ribeiro',
    author_email='adriano@xnv.io, nathan@xnv.io, thales@xnv.io',
    python_requires='>=3.7.0',
    include_package_data=True,
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
