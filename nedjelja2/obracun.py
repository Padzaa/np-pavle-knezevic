"""Poslovna logika: obračun iznosa. Nema I/O, pa se lako testira."""

from nedjelja2.modeli import Rezervacija


def izracunaj_iznos(rezervacija: Rezervacija) -> float:
    return rezervacija.kolicina * rezervacija.cijena
