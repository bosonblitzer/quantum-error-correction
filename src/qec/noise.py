
"""Independent bit-flip noise models for QEC simulations."""

import numpy as np
import numpy.typing as npt


def sample_bit_flip_errors(
    n_qubits: int,
    p: float,
    rng: np.random.Generator,
) -> npt.NDArray[np.int8]:
    """Sample independent bit-flip errors for physical qubits."""
    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1.")

    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be between 0 and 1.")

    return rng.binomial(1, p, size=n_qubits).astype(np.int8)
