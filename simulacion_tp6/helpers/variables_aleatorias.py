import random
from math import log as ln


def IA() -> int:
    r = 1
    while r == 1:
        r = random.uniform(0, 1)

    ia = -250.05660 * ln(1 - r)
    return round(ia)


def TAN() -> int:
    r = 1
    while r == 1:
        r = random.uniform(0, 1)

    tan = -298.72896 * ln(1 - r) + 101
    return round(tan)


def TAC() -> int:
    r = 1
    while r == 1:
        r = random.uniform(0, 1)

    tac = 309.79898 * ((-ln(1 - (r ** (1 / 0.96184)))) ** (1 / 1.00800)) + 101
    return round(tac)
