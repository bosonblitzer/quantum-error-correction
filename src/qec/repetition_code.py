
"""Three-qubit repetition-code syndrome calculations."""

import numpy as np
import numpy.typing as npt


def calculate_syndrome(
    errors: npt.ArrayLike,
) -> tuple[int, int]:
    """Calculate the two parity-check outcomes.

    Args:
        errors: Three binary values, where 1 represents a bit flip.

    Returns:
        (s1, s2), the two-bit error syndrome.
    """
    bits = np.asarray(errors)

    if bits.shape != (3,):
        raise ValueError("Exactly three error bits are required.")

    if not np.all(np.isin(bits, [0, 1])):
        raise ValueError("Error values must be binary (0 or 1).")

    e1, e2, e3 = (int(bit) for bit in bits)

    s1 = e1 ^ e2
    s2 = e2 ^ e3

    return s1, s2
