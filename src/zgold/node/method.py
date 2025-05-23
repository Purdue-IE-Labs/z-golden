from dataclasses import dataclass
from typing import Any, Self

@dataclass
class MethodConfig:
    path: str
    params: list[DataItemConfig]
    responses: list[DataItemConfig]
    props: list[Prop]
    handler: MethodHandler | None

    @classmethod
    def from_json5(cls, j: Any) -> Self:
        if not isinstance(j, dict):
            raise ValueError(f"Invalid method config {j}")
        if "path" not in j:
            raise LookupError(f"Method must specify path, {j}")
        path = j["path"]
        props = []
        for k, v in j.get("props", {}).items():
            props.append(Prop.from_json5(k,v))
        
