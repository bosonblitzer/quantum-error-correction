
import numpy as np
import pytest

from qec.noise import sample_bit_flip_errors


def test_zero_probability_never_flips():
    rng = np.random.default_rng(42)
    errors = sample_bit_flip_errors(100, 0.0, rng)

    assert np.all(errors == 0)


def test_unit_probability_always_flips():
    rng = np.random.default_rng(42)
    errors = sample_bit_flip_errors(100, 1.0, rng)

    assert np.all(errors == 1)


def test_output_has_expected_shape_and_values():
    rng = np.random.default_rng(42)
    errors = sample_bit_flip_errors(3, 0.2, rng)

    assert errors.shape == (3,)
    assert np.all(np.isin(errors, [0, 1]))


@pytest.mark.parametrize("p", [-0.1, 1.1])
def test_invalid_probability_raises(p):
    rng = np.random.default_rng(42)

    with pytest.raises(ValueError):
        sample_bit_flip_errors(3, p, rng)


def test_invalid_qubit_count_raises():
    rng = np.random.default_rng(42)

    with pytest.raises(ValueError):
        sample_bit_flip_errors(0, 0.1, rng)
