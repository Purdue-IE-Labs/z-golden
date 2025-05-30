from dataclasses import dataclass
from typing import Any, Self

from zgold.py_proto.type import Type
from zgold.py_proto.props import Prop

@dataclass
class DataItemConfig:
    path: str
    type: Type
    props: list[Prop]

    @classmethod
    def from_json5(cls, j: Any) -> Self:
        # import props
        if not isinstance(j, dict):
            raise ValueError(f"Data Item Config must be of type dictionary, found {j}")

        if "path" not in j:
            raise LookupError(f"Every tag must have a path! Tag provided with no keyword 'path': {j}")
        path = j["path"]
        type = Type.from_json5(j)
        props = [Prop.from_json5(key, p) for key, p in j.get("props", {}).items()]
        return cls(path, type, props)
 