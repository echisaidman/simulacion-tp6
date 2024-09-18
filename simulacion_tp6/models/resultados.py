from dataclasses import dataclass


@dataclass
class Resultados:
    CANT_JUNIORS: int
    CANT_SENIORS: int
    PECN: float
    PECC: float
    PARR: float
    PTOJ: list[float]
    PTOS: list[float]
