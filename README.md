# np-pavle-knezevic

Repozitorijum za predmet **Napredno programiranje (FIST4NP)**, Univerzitet Donja Gorica.
Isti repozitorijum se koristi za sve mini projekte i završni projekat.

## Okruženje

- Python 3.12+
- IDE: PyCharm (umjesto VS Code)
- Linter/formatter: [ruff](https://docs.astral.sh/ruff/)
- Testovi: [pytest](https://docs.pytest.org/)

## Pokretanje

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

ruff check .          # lint
ruff format --check . # provjera formatiranja
pytest                # testovi
```

## Sadržaj

- [Zadatak 1: `prosjecna_cijena`](#zadatak-1-prosjecna_cijena)
- [Nedjelja 2: Refaktoring klase sa više odgovornosti](nedjelja2/README.md)

## Zadatak 1: `prosjecna_cijena`

Funkcija se nalazi u [`cijene.py`](cijene.py), a testovi u [`tests/test_cijene.py`](tests/test_cijene.py).

```python
>>> from cijene import prosjecna_cijena
>>> prosjecna_cijena([10, 20, 30])
20.0
```

Funkcija prima niz cijena (int ili float) i vraća njihovu aritmetičku sredinu.
Baca `ValueError` za praznu listu, negativne cijene, NaN i beskonačnost, a `TypeError` za vrijednosti koje nisu brojevi.

### Upotrijebljeni upit

AI asistent: **Claude Code** (model Claude Opus), pokrenut u terminalu nad PyCharm projektom.

Upit (uz fotografiju slajda sa zadatkom):

> napravi sve ovo, imam vec github nalog povezan, koristi postojeci pycharm projekat i pycharm kao ide

Asistent je sam odlučio o potpisu funkcije, ponašanju na greškama i o testovima, jer upit to nije precizirao.

### Uočeni nedostaci generisanog koda

1. **Nejasna specifikacija, pretpostavljen ulaz.** Upit nije rekao šta funkcija prima. Asistent je pretpostavio listu brojeva. Ako se očekuje npr. lista proizvoda (`{"naziv": ..., "cijena": ..., "kolicina": ...}`) ili ponderisani prosjek po količini, funkcija ne radi ono što treba.
2. **`float` za novac.** Cijene se računaju kao `float`, pa su moguće greške zaokruživanja (npr. `0.1 + 0.2`). Za novac je prikladniji `decimal.Decimal`. Korišćen je `math.fsum`, što ublažava problem, ali ga ne rješava.
3. **Odbija `Decimal` i `Fraction`.** Provjera tipa dozvoljava samo `int` i `float`, pa `prosjecna_cijena([Decimal("9.99")])` baca `TypeError`, iako je `Decimal` upravo prirodan tip za cijene.
4. **Rezultat nije zaokružen.** Vraća se npr. `8.496666666666666`. Da li zaokružiti na 2 decimale (i kako: bankarsko ili klasično zaokruživanje) ostavljeno je pozivaocu, a to nije dokumentovano kao odluka specifikacije.
5. **Proizvoljna poslovna pravila.** Negativne cijene se odbijaju, a nula je dozvoljena. To je pretpostavka asistenta; u nekim domenima (povrati, popusti) negativni iznosi su validni.
6. **Cijeli ulaz se učitava u memoriju** (`list(cijene)`), što je nepotrebno za veoma velike nizove.
7. **Testove je napisao isti asistent koji je napisao kod**, pa testiraju njegove sopstvene pretpostavke, a ne nezavisnu specifikaciju. Npr. nema testa za `Decimal`, pa nedostatak iz tačke 3 testovi ne otkrivaju.
