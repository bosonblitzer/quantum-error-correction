
"""Minimum-weight decoder for the three-qubit repetition code."""

from qec.repetition_code import calculate_syndrome


def decode_syndrome(syndrome: tuple[int, int]) -> tuple[int, int, int]:
    """Return the estimated error pattern for a syndrome.

    The decoder assumes independent bit-flip errors with p < 0.5.
    The returned tuple contains 1 where a correction should be applied.
    """
    if (
        not isinstance(syndrome, (tuple, list))
        or len(syndrome) != 2
        or any(bit not in (0, 1) for bit in syndrome)
    ):
        raise ValueError("Syndrome must contain exactly two binary bits.")

    s1, s2 = syndrome

    if (s1, s2) == (0, 0):
        return (0, 0, 0)
    if (s1, s2) == (1, 0):
        return (1, 0, 0)
    if (s1, s2) == (1, 1):
        return (0, 1, 0)
    return (0, 0, 1)


def decode_errors(errors: tuple[int, int, int]) -> tuple[int, int, int]:
    """Estimate the error pattern directly from three error bits."""
    syndrome = calculate_syndrome(errors)
    return decode_syndrome(syndrome)
