import json

import pytest

from nedjelja2.izlaz import KonzolniObavjestavac, TxtIzvjestaj
from nedjelja2.izvori import CsvIzvor, JsonIzvor
from nedjelja2.modeli import Rezervacija
from nedjelja2.obracun import izracunaj_iznos
from nedjelja2.servis import ServisRezervacija


class ZamjenskiIzvor:
    """Izvor u memoriji: servis se testira bez fajlova."""

    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class ZapamtiSkladiste:
    def __init__(self) -> None:
        self.sacuvano: list[float] | None = None

    def sacuvaj(self, iznosi: list[float]) -> None:
        self.sacuvano = iznosi


class ZapamtiObavjestavac:
    def __init__(self) -> None:
        self.poslato: list[float] = []

    def posalji(self, ukupno: float) -> None:
        self.poslato.append(ukupno)


def napravi_servis(izvor):
    skladiste, obavjestavac = ZapamtiSkladiste(), ZapamtiObavjestavac()
    return ServisRezervacija(izvor, skladiste, obavjestavac), skladiste, obavjestavac


def test_izracunaj_iznos():
    assert izracunaj_iznos(Rezervacija("R1", 3, 40.0)) == 120.0


def test_servis_sa_zamjenskim_izvorom():
    izvor = ZamjenskiIzvor([Rezervacija("R1", 2, 50.0), Rezervacija("R2", 1, 30.5)])
    servis, skladiste, obavjestavac = napravi_servis(izvor)

    assert servis.obradi() == [100.0, 30.5]
    assert skladiste.sacuvano == [100.0, 30.5]
    assert obavjestavac.poslato == [130.5]


def test_servis_sa_praznim_izvorom():
    servis, skladiste, obavjestavac = napravi_servis(ZamjenskiIzvor([]))

    assert servis.obradi() == []
    assert skladiste.sacuvano == []
    assert obavjestavac.poslato == [0]


def test_csv_izvor(tmp_path):
    fajl = tmp_path / "rezervacije.csv"
    fajl.write_text("R1,2,50.0\nR2,1,30.5\n\n", encoding="utf-8")

    assert CsvIzvor(fajl).ucitaj() == [Rezervacija("R1", 2, 50.0), Rezervacija("R2", 1, 30.5)]


def test_csv_izvor_neispravan_red(tmp_path):
    fajl = tmp_path / "rezervacije.csv"
    fajl.write_text("R1,dva,50.0\n", encoding="utf-8")

    with pytest.raises(ValueError):
        CsvIzvor(fajl).ucitaj()


def test_json_izvor_radi_sa_istim_servisom(tmp_path):
    fajl = tmp_path / "rezervacije.json"
    fajl.write_text(json.dumps([{"oznaka": "R1", "kolicina": 4, "cijena": 25}]), encoding="utf-8")
    servis, skladiste, obavjestavac = napravi_servis(JsonIzvor(fajl))

    assert servis.obradi() == [100.0]
    assert obavjestavac.poslato == [100.0]


def test_csv_i_json_daju_isti_rezultat(tmp_path):
    csv_fajl = tmp_path / "r.csv"
    csv_fajl.write_text("R1,2,50.0\nR2,3,10.0\n", encoding="utf-8")
    json_fajl = tmp_path / "r.json"
    json_fajl.write_text(
        json.dumps(
            [
                {"oznaka": "R1", "kolicina": 2, "cijena": 50.0},
                {"oznaka": "R2", "kolicina": 3, "cijena": 10.0},
            ]
        ),
        encoding="utf-8",
    )

    assert (
        napravi_servis(CsvIzvor(csv_fajl))[0].obradi()
        == napravi_servis(JsonIzvor(json_fajl))[0].obradi()
    )


def test_txt_izvjestaj_i_konzola(tmp_path, capsys):
    izvjestaj = tmp_path / "izvjestaj.txt"
    TxtIzvjestaj(izvjestaj).sacuvaj([100.0, 30.5])
    KonzolniObavjestavac().posalji(130.5)

    assert izvjestaj.read_text(encoding="utf-8") == "[100.0, 30.5]"
    assert capsys.readouterr().out == "Poslato: 130.5\n"
