import math

import pytest

from cijene import prosjecna_cijena


def test_osnovni_slucaj():
    assert prosjecna_cijena([10, 20, 30]) == 20


def test_decimalne_cijene():
    assert prosjecna_cijena([9.99, 12.50, 3.00]) == pytest.approx(8.4966666, rel=1e-6)


def test_jedna_cijena():
    assert prosjecna_cijena([4.5]) == 4.5


def test_nula_je_dozvoljena():
    assert prosjecna_cijena([0, 0, 6]) == 2


def test_prihvata_bilo_koji_iterable():
    assert prosjecna_cijena(c for c in (1, 2, 3)) == 2
    assert prosjecna_cijena((5.0, 7.0)) == 6.0


def test_preciznost_sabiranja():
    # naivni sum([0.1] * 10) daje 0.9999999999999999
    assert prosjecna_cijena([0.1] * 10) == 0.1


def test_prazna_lista_baca_gresku():
    with pytest.raises(ValueError, match="prazna"):
        prosjecna_cijena([])


def test_negativna_cijena_baca_gresku():
    with pytest.raises(ValueError, match="negativna"):
        prosjecna_cijena([10, -5])


@pytest.mark.parametrize("losa", [math.nan, math.inf])
def test_nan_i_beskonacno(losa):
    with pytest.raises(ValueError, match="konačan"):
        prosjecna_cijena([1, losa])


@pytest.mark.parametrize("losa", ["10", None, True])
def test_nebrojevi_bacaju_type_error(losa):
    with pytest.raises(TypeError):
        prosjecna_cijena([1, losa])
