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


from .singleton import SingletonDecorator
import uuid


@SingletonDecorator
class Theorem:
    """
    Singleton class responsible act as a single source of truth regarding the experiment change's state
    Eg. inform that the source-code has changed
    """

    def __init__(self):
        self.requirements_changed = False
        self.code_changed = False
        self.dataset_changed = False
        self.parameters_changed = False
        self.experiment_id = str(uuid.uuid4())

    def has_any_change(self):
        return self.requirements_changed is not False or self.code_changed is not False or \
               self.dataset_changed is not False or self.parameters_changed is not False

    def requirements_did_change(self, requirements_metadata_location_hash: str) -> None:
        self.requirements_changed = requirements_metadata_location_hash

    def code_did_change(self, code_metadata_location_hash: str) -> None:
        self.code_changed = code_metadata_location_hash

    def dataset_did_change(self, dataset_metadata_location_hash: str) -> None:
        self.dataset_changed = dataset_metadata_location_hash

    def parameters_did_change(self, parameters_metadata_location_hash: str) -> None:
        self.parameters_changed = parameters_metadata_location_hash
