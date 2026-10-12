
import pytest

from qec.decoder import decode_syndrome, decode_errors


@pytest.mark.parametrize(
    ("syndrome", "expected"),
    [
        ((0, 0), (0, 0, 0)),
        ((1, 0), (1, 0, 0)),
        ((1, 1), (0, 1, 0)),
        ((0, 1), (0, 0, 1)),
    ],
)
def test_syndrome_decoding(syndrome, expected):
    assert decode_syndrome(syndrome) == expected


@pytest.mark.parametrize(
    "errors",
    [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    ],
)
def test_all_single_bit_flips_are_identified(errors):
    assert decode_errors(errors) == errors


@pytest.mark.parametrize(
    "syndrome",
    [
        (0,),
        (0, 0, 0),
        (0, 2),
        (-1, 0),
    ],
)
def test_invalid_syndromes_raise(syndrome):
    with pytest.raises(ValueError):
        decode_syndrome(syndrome)
