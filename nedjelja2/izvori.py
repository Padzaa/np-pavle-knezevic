"""Izvori podataka. Servis zavisi samo od protokola IzvorRezervacija (princip D)."""

import csv
import json
from pathlib import Path
from typing import Protocol

from nedjelja2.modeli import Rezervacija


class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class CsvIzvor:
    """Čita CSV redove oblika ``oznaka,kolicina,cijena`` (format originalnog koda)."""

    def __init__(self, putanja: str | Path) -> None:
        self.putanja = Path(putanja)

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(encoding="utf-8", newline="") as f:
            return [
                Rezervacija(oznaka=red[0].strip(), kolicina=int(red[1]), cijena=float(red[2]))
                for red in csv.reader(f)
                if red
            ]


class JsonIzvor:
    """Drugi izvor, dodat bez ikakve izmjene servisa (princip O).

    Očekuje listu objekata: ``[{"oznaka": "R1", "kolicina": 2, "cijena": 45.0}, ...]``.
    """

    def __init__(self, putanja: str | Path) -> None:
        self.putanja = Path(putanja)

    def ucitaj(self) -> list[Rezervacija]:
        podaci = json.loads(self.putanja.read_text(encoding="utf-8"))
        return [
            Rezervacija(
                oznaka=str(p["oznaka"]), kolicina=int(p["kolicina"]), cijena=float(p["cijena"])
            )
            for p in podaci
        ]
