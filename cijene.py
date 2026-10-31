"""Pomoćne funkcije za rad sa cijenama."""

import math
from collections.abc import Iterable


def prosjecna_cijena(cijene: Iterable[float]) -> float:
    """Vrati aritmetičku sredinu datih cijena.

    Args:
        cijene: niz cijena (int ili float), npr. ``[9.99, 12.50, 3.00]``.

    Returns:
        Prosječna cijena kao float (nezaokružena).

    Raises:
        ValueError: ako je niz prazan, ili sadrži negativnu, NaN ili beskonačnu cijenu.
        TypeError: ako neki element nije broj (bool se ne prihvata kao broj).
    """
    vrijednosti = list(cijene)
    if not vrijednosti:
        raise ValueError("Lista cijena ne smije biti prazna.")

    for c in vrijednosti:
        if isinstance(c, bool) or not isinstance(c, int | float):
            raise TypeError(f"Cijena mora biti broj, dobijeno: {c!r}")
        if not math.isfinite(c):
            raise ValueError(f"Cijena mora biti konačan broj, dobijeno: {c!r}")
        if c < 0:
            raise ValueError(f"Cijena ne smije biti negativna, dobijeno: {c!r}")

    return math.fsum(vrijednosti) / len(vrijednosti)
