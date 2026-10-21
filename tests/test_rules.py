from rules import ensure_weight_fits


def test_empty_weights_with_new_weight_of_50_fits():
    ensure_weight_fits([], 50)