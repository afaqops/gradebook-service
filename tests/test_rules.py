from rules import ensure_weight_fits


def test_empty_weights_with_new_weight_of_50_fits():
    ensure_weight_fits([], 50)

    
from rules import ensure_weight_fits


def test_empty_weights_with_new_weight_of_50_fits():
    ensure_weight_fits([], 50)


def test_weight_that_exceeds_100_is_rejected():
    import pytest
    from errors import ValidationError

    with pytest.raises(ValidationError):
        ensure_weight_fits([], 101)



import pytest

from errors import ValidationError
from rules import ensure_weight_fits


def test_empty_weights_with_new_weight_of_50_fits():
    ensure_weight_fits([], 50)


def test_weight_that_exceeds_100_is_rejected():
    with pytest.raises(ValidationError):
        ensure_weight_fits([], 101)


def test_weight_total_of_100_fits():
    ensure_weight_fits([60], 40)

def test_decimal_weights_that_total_100_fit():
    ensure_weight_fits([9.3, 27.3, 33.7], 29.7)