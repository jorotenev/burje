import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any


class CreatableFromStrEnumMixin:
    """
    note that the mixin should be put first in the inheritance list:
    class SomeEnum(CreatableFromStrEnumMixin, enums.Enum):
        pass
    """

    @classmethod
    def from_str(cls, name):
        lowered = name.lower()
        if lowered not in cls.__dict__:
            raise ValueError(f'name={name} is not a valid {cls.__name__}')
        return getattr(cls, lowered)

    @classmethod
    def enum_has_name(cls, name):
        return name.lower() in {enum_name.lower() for enum_name in cls.__dict__}


class Unit(CreatableFromStrEnumMixin, Enum):
    seconds = 'seconds'
    microseconds = 'microseconds'
    milliseconds = 'milliseconds'
    bytes = 'bytes'
    kilobytes = 'kilobytes'
    megabytes = 'megabytes'

    def __json__(self):
        return


@dataclass
class Measurement:
    created_at: datetime
    metric: str
    dimensions: Dict[str, Any]
    value: Any
    unit: Unit

    def to_json(self):
        d = asdict(self)
        d['created_at'] = self.created_at.isoformat()
        d['unit'] = self.unit.name
        return json.dumps(d)
