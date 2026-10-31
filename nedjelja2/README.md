# Nedjelja 2: Refaktoring klase sa više odgovornosti

Polazni kod sa slajda je sačuvan u [`obrada_original.py`](obrada_original.py), samo radi poređenja.

## 1. Identifikovati odgovornosti (princip S)

Klasa `UpravljanjeRezervacijama` ima **četiri razloga za promjenu**:

| Odgovornost | Metoda | Mijenja se kad se promijeni... |
|---|---|---|
| Čitanje i parsiranje podataka | `ucitaj` | format ili izvor podataka (CSV, JSON, baza) |
| Poslovni obračun | `izracunaj_iznos` | pravilo obračuna (popust, PDV) |
| Čuvanje izvještaja | `sacuvaj_izvjestaj` | format ili mjesto izvještaja |
| Obavještavanje | `posalji_mail` | način slanja (mail, SMS, konzola) |

Usput uočeni problemi u originalu:
- `open(...)` bez `with`, pa se fajlovi ne zatvaraju eksplicitno.
- Putanja `izvjestaj.txt` je zakucana u kodu.
- `posalji_mail` ne šalje mail, samo štampa.
- Red je lista stringova (`r[1]`, `r[2]`), pa je nejasno šta je koja kolona.
- Nijedna metoda ne poziva ostale, a ne postoji ni mjesto koje ih spaja u tok obrade.

## 2. Razdvojiti

| Fajl | Sadržaj |
|---|---|
| [`modeli.py`](modeli.py) | `Rezervacija` (dataclass sa imenovanim poljima umjesto `r[1]`, `r[2]`) |
| [`obracun.py`](obracun.py) | `izracunaj_iznos`, čista funkcija bez I/O |
| [`izvori.py`](izvori.py) | `CsvIzvor`, `JsonIzvor` |
| [`izlaz.py`](izlaz.py) | `TxtIzvjestaj`, `KonzolniObavjestavac` |
| [`servis.py`](servis.py) | `ServisRezervacija`: učitaj → obračunaj → sačuvaj → obavijesti |

## 3. Apstrahovati izvor kroz Protocol (princip D)

```python
class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...
```

`ServisRezervacija` prima izvor kroz konstruktor i zavisi samo od protokola, a ne od konkretne klase. Na isti način su apstrahovani i `SkladisteIzvjestaja` i `Obavjestavac`.

## 4. Proširiti drugim izvorom (princip O)

Dodat je `JsonIzvor`, a `servis.py` nije mijenjan. Test `test_csv_i_json_daju_isti_rezultat` pokazuje da isti servis daje isti rezultat sa oba izvora.

```python
servis = ServisRezervacija(JsonIzvor("rezervacije.json"), TxtIzvjestaj(), KonzolniObavjestavac())
servis.obradi()
```

## 5. Testirati sa zamjenskim izvorom

Testovi su u [`tests/nedjelja2/test_servis.py`](../tests/nedjelja2/test_servis.py). `ZamjenskiIzvor` drži rezervacije u memoriji, a `ZapamtiSkladiste` i `ZapamtiObavjestavac` pamte šta im je servis predao. Zato se servis testira bez ijednog fajla. Zamjenske klase ne nasljeđuju protokol, nego ga zadovoljavaju samim oblikom (strukturno tipiziranje).

## 6. Poređenje sa prijedlogom AI asistenta

Ovo rješenje je generisao AI asistent (Claude Code), na osnovu fotografije slajda i upita „odradi ovo“.

<!-- TODO: dopuniti poređenjem sa rješenjem urađenim u paru na vježbama. -->

Odluke koje je asistent donio i koje vrijedi preispitati:
- **Možda previše fajlova za mali primjer.** Pet modula za dvadesetak linija logike je mnogo. Jednostavnija varijanta bi bila jedan fajl sa nekoliko klasa i funkcija.
- **Protokoli i za izlaz, ne samo za izvor.** Zadatak traži Protocol samo za izvor podataka. Asistent ga je dodao i za izvještaj i obavještavanje, da bi test servisa bio bez fajlova i bez `print`-a.
- **Pretpostavljena značenja kolona.** Original ne kaže šta su `r[0]`, `r[1]` i `r[2]`. Asistent ih je nazvao `oznaka`, `kolicina` i `cijena`, što je pretpostavka.
- **Ponašanje se neznatno promijenilo:** CSV se čita preko modula `csv`, pa se navodnici i prazni redovi obrađuju drugačije nego sa `split(",")`, a obavještenje dobija već izračunat zbir.
- **Neispravni podaci se ne validiraju.** Za neispravan red parsiranje baca `ValueError` i obrada se prekida. Ne postoji preskakanje loših redova niti poruka o tome koji red je neispravan.
