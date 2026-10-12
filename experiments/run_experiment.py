

"""Monte Carlo evaluation of the three-qubit repetition code."""

import csv
from pathlib import Path

import numpy as np

from qec.decoder import decode_syndrome
from qec.noise import sample_bit_flip_errors
from qec.repetition_code import calculate_syndrome


def theoretical_logical_error_rate(p: float) -> float:
    """Probability that majority voting fails for three qubits."""
    return 3 * p**2 * (1 - p) + p**3


def wilson_interval(
    successes: int,
    trials: int,
    z: float = 1.96,
) -> tuple[float, float]:
    """Calculate a two-sided Wilson confidence interval for a proportion."""
    if trials < 1:
        raise ValueError("Trials must be at least 1.")
    if not 0 <= successes <= trials:
        raise ValueError("Successes must be between 0 and trials.")

    estimate = successes / trials
    z_squared = z**2
    denominator = 1 + z_squared / trials

    centre = (
        estimate + z_squared / (2 * trials)
    ) / denominator

    margin = (
        z
        * np.sqrt(
            estimate * (1 - estimate) / trials
            + z_squared / (4 * trials**2)
        )
        / denominator
    )

    return max(0.0, centre - margin), min(1.0, centre + margin)


def run_experiment(
    error_rates: list[float],
    n_trials: int = 100_000,
    seed: int = 42,
) -> list[dict[str, float]]:
    """Estimate physical and logical error rates by simulation."""
    if n_trials < 1:
        raise ValueError("n_trials must be at least 1.")

    rng = np.random.default_rng(seed)
    results = []

    for p in error_rates:
        if not 0.0 <= p <= 1.0:
            raise ValueError("Error probabilities must be between 0 and 1.")

        physical_errors = 0
        logical_errors = 0

        for _ in range(n_trials):
            errors = sample_bit_flip_errors(3, p, rng)
            physical_errors += int(np.sum(errors))

            syndrome = calculate_syndrome(errors)
            correction = decode_syndrome(syndrome)

            residual_errors = errors ^ np.array(
                correction, dtype=np.int8
            )

            # A residual odd number of flips corrupts the logical bit.
            if int(np.sum(residual_errors)) % 2 == 1:
                logical_errors += 1

        logical_rate = logical_errors / n_trials
        ci_low, ci_high = wilson_interval(logical_errors, n_trials)

        
        physical_rate = physical_errors / (3 * n_trials)

        
        results.append(
            {
                "p": p,
                "physical_error_rate": physical_rate,
                "logical_errors": logical_errors,
                "logical_error_rate": logical_rate,
                "ci_95_lower": ci_low,
                "ci_95_upper": ci_high,
                "theoretical_logical_error_rate":
                    theoretical_logical_error_rate(p),
                "error_reduction_factor": (
                    physical_rate / logical_rate
                    if logical_rate > 0
                    else float("inf")
                ),
                "relative_error_reduction": (
                    1 - logical_rate / physical_rate
                    if physical_rate > 0
                    else 0.0
                ),
            }
        )
    return results


def main() -> None:
    error_rates = [0.01, 0.03, 0.05, 0.10, 0.15, 0.20]
    n_trials = 100_000
    results = run_experiment(error_rates, n_trials=n_trials)

    output_path = Path("results") / "repetition_code_results.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Trials per error rate: {n_trials:,}")
    print(f"Results saved to: {output_path.resolve()}")
    print()
    
    print(
        f"{'p':>5} {'Physical':>10} {'Logical':>10} "
        f"{'Theory':>10} {'Reduction':>11} {'Errors cut':>11}"
    )

    for result in results:
        print(
            f"{result['p']:5.2f} "
            f"{result['physical_error_rate']:10.5f} "
            f"{result['logical_error_rate']:10.5f} "
            f"{result['theoretical_logical_error_rate']:10.5f} "
            f"{result['error_reduction_factor']:10.2f}x "
            f"{100 * result['relative_error_reduction']:10.1f}%"
        )



if __name__ == "__main__":
    main()
