from dataclasses import dataclass
from .base_type import BaseType


@dataclass
class Prop:
    key: str
    value: BaseData
