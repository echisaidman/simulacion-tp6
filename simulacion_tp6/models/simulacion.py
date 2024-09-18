import random
from typing import Literal

from simulacion_tp6.helpers.constantes import HV
from simulacion_tp6.helpers.variables_aleatorias import IA, TAC, TAN

from .resultados import Resultados

NormalCritico = Literal["Normal", "Critico"]


class Simulacion:
    def __init__(
        self, cant_juniors: int, cant_seniors: int, tiempo_total_simulacion: int
    ) -> None:
        self.CANT_JUNIORS = cant_juniors
        self.CANT_SENIORS = cant_seniors
        self.TIEMPO_FINAL = tiempo_total_simulacion
        self.__condiciones_iniciales()

    def __condiciones_iniciales(self) -> None:
        self.T = 0
        self.TPLL = 0
        self.TPSJ = [HV] * self.CANT_JUNIORS
        self.TPSS = [HV] * self.CANT_SENIORS
        self.NSJ = self.NSS = 0
        self.NTN = self.NTC = 0
        self.TTS: list[NormalCritico] = ["Critico"] * self.CANT_SENIORS
        self.ITOJ = [0] * self.CANT_JUNIORS
        self.ITOS = [0] * self.CANT_SENIORS
        self.STLLN = self.STSN = self.STAN = 0
        self.STLLC = self.STSC = self.STAC = 0
        self.STOJ = [0] * self.CANT_JUNIORS
        self.STOS = [0] * self.CANT_SENIORS
        self.NARR = 0

    def simular(self) -> Resultados:
        while True:
            s = self.__senior_menor_tps()
            j = self.__junior_menor_tps()

            if self.TPSS[s] <= self.TPSJ[j]:
                if self.TPLL <= self.TPSS[s]:
                    self.__llegada()
                else:
                    self.__salida_senior(s)
            else:
                if self.TPLL <= self.TPSJ[j]:
                    self.__llegada()
                else:
                    self.__salida_junior(j)

            if self.T > self.TIEMPO_FINAL:
                if self.NSJ + self.NSS > 0:
                    # Vaciamiento
                    self.TPLL = HV
                else:
                    break

        return self.__calcular_resultados()

    def __senior_menor_tps(self) -> int:
        senior_menor_tps = 0
        for i in range(len(self.TPSS)):
            if self.TPSS[i] <= self.TPSS[senior_menor_tps]:
                senior_menor_tps = i
        return senior_menor_tps

    def __junior_menor_tps(self) -> int:
        junior_menor_tps = 0
        for i in range(len(self.TPSJ)):
            if self.TPSJ[i] <= self.TPSJ[junior_menor_tps]:
                junior_menor_tps = i
        return junior_menor_tps

    def __llegada(self) -> None:
        self.T = self.TPLL
        ia = IA()
        self.TPLL = self.T + ia

        r = random.uniform(0, 1)
        if r <= 0.80:
            self.__llegada_ticket_normal()
        else:
            self.__llegada_ticket_critico()

    def __llegada_ticket_normal(self) -> None:
        if self.__arrepentimiento():
            self.NARR += 1
            return

        self.NTN += 1
        self.NSJ += 1  # El ticket normal va por defecto a la cola de los Juniors, pero despues puede pasarse a la de los Seniors
        self.STLLN += self.T

        if self.NSJ <= self.CANT_JUNIORS:
            # El ticket normal se atiende con un Junior
            x = self.__junior_libre_mayor_sto()
            self.STOJ[x] += self.T - self.ITOJ[x]
            tan = TAN()
            self.STAN += tan
            self.TPSJ[x] = self.T + tan
        elif self.NSJ == self.CANT_JUNIORS + 11 and self.NSS < self.CANT_SENIORS:
            # El ticket normal se atiende con un Senior (lo paso de cola)
            self.NSJ -= 1
            self.NSS += 1
            y = self.__senior_libre_mayor_sto()
            self.STOS[y] += self.T - self.ITOS[y]
            tan = TAN()
            self.STAN += tan
            self.TPSS[y] = self.T + tan
            self.TTS[y] = "Normal"

    def __arrepentimiento(self) -> bool:
        if self.NSJ <= (self.CANT_JUNIORS + 15):
            # Hay 15 tickets o menos en la cola, no hay arrepentimiento
            return False

        r = random.uniform(0, 1)
        # TODO: ver que porcentaje de arrepentimiento usamos
        arr = r <= 0.60
        return arr

    def __junior_libre_mayor_sto(self) -> int:
        primer_junior_libre = 0
        while self.TPSJ[primer_junior_libre] != HV:
            primer_junior_libre += 1

        junior_libre_mayor_sto = primer_junior_libre
        for i in range(junior_libre_mayor_sto, self.CANT_JUNIORS):
            if self.TPSJ[i] == HV and self.STOJ[i] >= self.STOJ[junior_libre_mayor_sto]:
                junior_libre_mayor_sto = i
        return junior_libre_mayor_sto

    def __senior_libre_mayor_sto(self) -> int:
        primer_senior_libre = 0
        while self.TPSS[primer_senior_libre] != HV:
            primer_senior_libre += 1

        senior_libre_mayor_sto = primer_senior_libre
        for i in range(senior_libre_mayor_sto, self.CANT_SENIORS):
            if self.TPSS[i] == HV and self.STOS[i] >= self.STOS[senior_libre_mayor_sto]:
                senior_libre_mayor_sto = i
        return senior_libre_mayor_sto

    def __llegada_ticket_critico(self) -> None:
        self.NTC += 1
        self.NSS += 1
        self.STLLC += self.T

        if self.NSS <= self.CANT_SENIORS:
            y = self.__senior_libre_mayor_sto()
            self.STOS[y] += self.T - self.ITOS[y]
            tac = TAC()
            self.STAC += tac
            self.TPSS[y] = self.T + tac
            self.TTS[y] = "Critico"

    def __salida_junior(self, j: int) -> None:
        self.T = self.TPSJ[j]
        self.NSJ -= 1
        self.STSN += self.T

        if self.NSJ >= self.CANT_JUNIORS:
            # Hay mas tickets en la cola, el puesto j atiende a otro
            tan = TAN()
            self.STAN += tan
            self.TPSJ[j] = self.T + tan
        else:
            # No hay mas tickets, el puesto queda ocioso
            self.ITOJ[j] = self.T
            self.TPSJ[j] = HV

    def __salida_senior(self, s: int) -> None:
        self.T = self.TPSS[s]
        self.NSS -= 1

        if self.TTS[s] == "Normal":
            # El Senior termino de atender un ticket normal
            self.STSN += self.T
        else:
            # El Senior termino de atender un ticket critico
            self.STSC += self.T

        if self.NSS >= self.CANT_SENIORS:
            # Hay mas tickets (criticos) en la cola, el puesto s atiende a otro
            tac = TAC()
            self.STAC += tac
            self.TPSS[s] = self.T + tac
            self.TTS[s] = "Critico"
        elif self.NSJ >= self.CANT_JUNIORS + 11:
            # El puesto s atiende a un ticket normal (se lo saca a los Juniors)
            self.NSJ -= 1
            self.NSS += 1
            tan = TAN()
            self.STAN += tan
            self.TPSS[s] = self.T + tan
            self.TTS[s] = "Normal"
        else:
            # No hay mas tickets, el puesto queda ocioso
            self.ITOS[s] = self.T
            self.TPSS[s] = HV

    def __calcular_resultados(self) -> Resultados:
        return Resultados(
            CANT_JUNIORS=self.CANT_JUNIORS,
            CANT_SENIORS=self.CANT_SENIORS,
            PECN=(self.STSN - self.STLLN - self.STAN) / self.NTN,
            PECC=(self.STSC - self.STLLC - self.STAC) / self.NTC,
            PARR=(self.NARR / (self.NTN + self.NARR)) * 100,
            PTOJ=[(self.STOJ[j] / self.T) * 100 for j in range(self.CANT_JUNIORS)],
            PTOS=[(self.STOS[s] / self.T) * 100 for s in range(self.CANT_SENIORS)],
        )
