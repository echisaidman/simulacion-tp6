from dataclasses import dataclass
from typing import Any, cast


@dataclass
class Resultados:
    CANT_JUNIORS: int
    CANT_SENIORS: int
    PECN: float
    PECC: float
    PARR: float
    PTOJ: list[float]
    PTOS: list[float]

    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if isinstance(value, float):
            value = round(value, 3)
        elif isinstance(value, list):
            value = cast(list[Any], value)
            if len(value) > 0 and isinstance(value[0], float):
                value = cast(list[float], value)
                value = [round(v, 3) for v in value]
        return value
