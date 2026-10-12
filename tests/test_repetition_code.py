
import pytest

from qec.repetition_code import calculate_syndrome


@pytest.mark.parametrize(
    ("errors", "expected"),
    [
        ([0, 0, 0], (0, 0)),  # No error
        ([1, 0, 0], (1, 0)),  # Qubit 1 flipped
        ([0, 1, 0], (1, 1)),  # Qubit 2 flipped
        ([0, 0, 1], (0, 1)),  # Qubit 3 flipped
    ],
)
def test_single_error_syndromes(errors, expected):
    assert calculate_syndrome(errors) == expected



def test_two_flips_can_mimic_single_flip_syndrome():
    two_flips = calculate_syndrome([1, 1, 0])
    single_flip = calculate_syndrome([0, 0, 1])

    assert two_flips == single_flip



@pytest.mark.parametrize(
    "errors",
    [
        [0, 0],
        [0, 0, 0, 0],
        [0, 2, 0],
        [0, -1, 0],
    ],
)
def test_invalid_error_patterns_raise(errors):
    with pytest.raises(ValueError):
        calculate_syndrome(errors)
