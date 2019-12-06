"""
MetaData objects allow a user to:
  - dynamically add instance attributes and have them be json serializable.
  - serialize: convert json string naive(str only) MetaData object.
  - deserialize: convert MetaData object to json string.
  - save: perform a deserialization and save to file.
"""
import json
import logging
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Collection, Mapping, Union
from uuid import UUID


def _isinstance_safe(o, t):
    try:
        result = isinstance(o, t)
    except Exception:
        return False
    else:
        return result


Json = Union[dict, list, str, int, float, bool, None]


class _ExtendedEncoder(json.JSONEncoder):
    def default(self, o) -> Json:
        result: Json
        if _isinstance_safe(o, Collection):
            if _isinstance_safe(o, Mapping):
                result = dict(o)
            else:
                result = list(o)
        elif _isinstance_safe(o, datetime):
            result = o.timestamp()
        elif _isinstance_safe(o, UUID):
            result = str(o)
        elif _isinstance_safe(o, Enum):
            result = o.value
        elif _isinstance_safe(o, Decimal):
            result = str(o)
        else:
            result = json.JSONEncoder.default(self, o)
        return result


class MetaData:

    def serialize(self) -> str:
        """convert MetaData object to json string."""
        return json.dumps(self.__dict__, cls=_ExtendedEncoder)

    def deserialize(self, raw_json: str):
        """convert a json string to MetaData object."""

        json_obj = json.loads(raw_json)

        for k, v in json_obj.items():
            setattr(self, k, v)

    def save(self, destination: str) -> str:
        """perform a serialization and save to file"""

        with open(destination, "w+") as f:
            logging.info(f"saving file: {destination}")
            f.write(self.serialize())

        return destination
