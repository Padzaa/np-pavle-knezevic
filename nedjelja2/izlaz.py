"""Čuvanje izvještaja i slanje obavještenja, svako iza svog protokola."""

from pathlib import Path
from typing import Protocol


class SkladisteIzvjestaja(Protocol):
    def sacuvaj(self, iznosi: list[float]) -> None: ...


class Obavjestavac(Protocol):
    def posalji(self, ukupno: float) -> None: ...


class TxtIzvjestaj:
    def __init__(self, putanja: str | Path = "izvjestaj.txt") -> None:
        self.putanja = Path(putanja)

    def sacuvaj(self, iznosi: list[float]) -> None:
        self.putanja.write_text(str(iznosi), encoding="utf-8")


class KonzolniObavjestavac:
    """Original se zvao ``posalji_mail``, ali je samo štampao. Ime sad kaže šta radi."""

    def posalji(self, ukupno: float) -> None:
        print("Poslato:", ukupno)
