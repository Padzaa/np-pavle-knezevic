"""Domenski model: jedna rezervacija."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rezervacija:
    oznaka: str
    kolicina: int
    cijena: float
