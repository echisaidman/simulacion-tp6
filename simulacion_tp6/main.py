import datetime

import dateutil.tz
import pandas as pd
from pandas import DataFrame

from simulacion_tp6.models.resultados import Resultados
from simulacion_tp6.models.simulacion import Simulacion

PRESUPUESTO_TOTAL = 10_000_000
COSTO_JUNIOR = 500_000
COSTO_SENIOR = 1_500_000

TIEMPO_TOTAL_SIMULACION = 365 * 24 * 60 * 60


def main():
    todos_los_resultados: list[Resultados] = []

    for cant_juniors in range(1, 5):
        for cant_seniors in range(1, 5):
            print(f"Evaluando alternativa (J={cant_juniors}, S={cant_seniors})...")

            costo = cant_juniors * COSTO_JUNIOR + cant_seniors * COSTO_SENIOR
            if costo > PRESUPUESTO_TOTAL:
                # La alternativa esta por encima del presupuesto, me la salteo
                continue

            simulacion = Simulacion(cant_juniors, cant_seniors, TIEMPO_TOTAL_SIMULACION)
            resultados = simulacion.simular()

            todos_los_resultados.append(resultados)

    _guardar_resultados_en_excel(todos_los_resultados)
    print("Los resultados se guardaron correctamente en el Excel.")


def _guardar_resultados_en_excel(resultados: list[Resultados]) -> None:
    file_path = "./static/resultados.xlsx"

    df = _resultados_to_df(resultados)
    sheet_name = _get_excel_sheet_name()

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="a") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


def _resultados_to_df(resultados: list[Resultados]) -> DataFrame:
    return DataFrame(
        {
            "CANT_JUNIORS": [r.CANT_JUNIORS for r in resultados],
            "CANT_SENIORS": [r.CANT_SENIORS for r in resultados],
            "PECN": [r.PECN for r in resultados],
            "PECC": [r.PECC for r in resultados],
            "PARR": [r.PARR for r in resultados],
            "PTOJ": ["  ,  ".join([f"{ptoj}" for ptoj in r.PTOJ]) for r in resultados],
            "PTOS": ["  ,  ".join(f"{ptos}" for ptos in r.PTOS) for r in resultados],
        }
    )


def _get_excel_sheet_name() -> str:
    local_datetime = datetime.datetime.now(
        dateutil.tz.gettz("America/Argentina/Buenos_Aires")
    ).strftime(r"%Y%m%d_%H%M%S")
    return local_datetime
