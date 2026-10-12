
"""Plot logical error rates with 95% confidence intervals."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_PATH = Path("results/repetition_code_results.csv")
OUTPUT_PATH = Path("results/logical_error_comparison.png")


def main() -> None:
    with RESULTS_PATH.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    p = [float(row["p"]) for row in rows]
    simulated = [
        float(row["logical_error_rate"]) for row in rows
    ]
    theoretical = [
        float(row["theoretical_logical_error_rate"]) for row in rows
    ]
    lower = [float(row["ci_95_lower"]) for row in rows]
    upper = [float(row["ci_95_upper"]) for row in rows]

    lower_errors = [
        rate - bound for rate, bound in zip(simulated, lower)
    ]
    upper_errors = [
        bound - rate for rate, bound in zip(simulated, upper)
    ]

    plt.figure(figsize=(9, 6))

    plt.errorbar(
        p,
        simulated,
        yerr=[lower_errors, upper_errors],
        fmt="o",
        capsize=4,
        label="Monte Carlo (95% CI)",
    )
    plt.plot(
        p,
        theoretical,
        "s--",
        label="Theoretical logical error rate",
    )
    plt.plot(
        p,
        p,
        ":",
        label="Uncorrected physical error rate",
    )

    plt.xlabel("Physical bit-flip probability")
    plt.ylabel("Error probability")
    plt.title("Three-Qubit Repetition Code: Error Suppression")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    print(f"Plot saved to: {OUTPUT_PATH.resolve()}")

    plt.show()


if __name__ == "__main__":
    main()
