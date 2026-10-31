"""Servis koji orkestrira obradu. Ne zna odakle dolaze podaci ni gdje idu."""

from nedjelja2.izlaz import Obavjestavac, SkladisteIzvjestaja
from nedjelja2.izvori import IzvorRezervacija
from nedjelja2.obracun import izracunaj_iznos


class ServisRezervacija:
    def __init__(
        self,
        izvor: IzvorRezervacija,
        skladiste: SkladisteIzvjestaja,
        obavjestavac: Obavjestavac,
    ) -> None:
        self.izvor = izvor
        self.skladiste = skladiste
        self.obavjestavac = obavjestavac

    def obradi(self) -> list[float]:
        iznosi = [izracunaj_iznos(r) for r in self.izvor.ucitaj()]
        self.skladiste.sacuvaj(iznosi)
        self.obavjestavac.posalji(sum(iznosi))
        return iznosi
