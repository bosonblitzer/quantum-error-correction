# Quantum Error Correction: Three-Qubit Repetition Code

A Python simulation investigating how a three-qubit repetition code suppresses independent bit-flip errors. The project implements syndrome calculation, minimum-weight decoding, Monte Carlo experiments and statistical comparisons between simulated and theoretical logical error rates.

## Overview

Quantum error correction (QEC) uses redundancy to protect quantum information against errors. This project studies the three-qubit repetition code under an independent bit-flip noise model, examining how physical error probability affects logical failure probability.

The simulation compares empirical results against the theoretical prediction and uses 95% Wilson confidence intervals to quantify statistical uncertainty.

## Key Results

- Simulated **100,000 Monte Carlo trials** at each of six physical error probabilities, from 0.01 to 0.20.
- Implemented syndrome-based decoding using the minimum-weight correction for the three-qubit repetition code.
- Compared simulated logical error rates with theoretical predictions and calculated 95% Wilson confidence intervals.
- Observed a **96.9% reduction in error rate** at a physical error probability of 0.01, decreasing to 47.0% at 0.20.

## Results

The plot compares the simulated logical error rates with the theoretical prediction and the uncorrected physical error baseline.

![Simulated and theoretical logical error rates](results/logical_error_comparison.png)

The theoretical logical failure probability under independent bit-flip noise and perfect correction is

$$
P_{\mathrm{logical}} = 3p^2(1-p)+p^3
$$


Simplifying gives

$$
P_{\mathrm{logical}} = 3p^2 - 2p^3
$$

where $p$ is the physical bit-flip probability. A logical failure occurs when two or more of the three physical qubits experience bit flips.
$$
P_{\mathrm{logical}} = 3p^2 - 2p^3,
$$
where \(p\) is the physical bit-flip probability. A logical failure occurs when two or more of the three physical qubits experience bit flips.

## Methodology

1. **Noise model:** Sample independent bit-flip errors for three physical qubits using NumPy.
2. **Syndrome calculation:** Compute two parity checks to identify the error syndrome.
3. **Decoding:** Apply a minimum-weight correction based on the measured syndrome.
4. **Monte Carlo simulation:** Repeat the experiment across 100,000 trials per physical error probability.
5. **Statistical analysis:** Compare the simulated logical error rate against theory and calculate 95% Wilson confidence intervals.

## Project Structure

```text
quantum_error_correction/
├── experiments/
│   ├── run_experiment.py
│   └── plot_results.py
├── src/
│   └── qec/
│       ├── noise.py
│       ├── repetition_code.py
│       └── decoder.py
├── tests/
├── results/
│   ├── repetition_code_results.csv
│   └── logical_error_comparison.png
├── REPORT.md
├── pyproject.toml
└── requirements.txt
```

## Installation

Clone the repository and navigate to the project directory. Create and activate a virtual environment, then install the project and its dependencies.

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies and project:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Running the Project

Run the Monte Carlo experiment:

```bash
python -m experiments.run_experiment
```

Generate the results plot:

```bash
python -m experiments.plot_results
```

Run the test suite:

```bash
python -m pytest -v
```

The experiment writes the numerical results to `results/repetition_code_results.csv`. The plotting script generates `results/logical_error_comparison.png`.

## Limitations

This project models bit-flip errors using a classical error-pattern simulation. It does not simulate full quantum states or circuits, phase-flip errors, noisy syndrome measurements, imperfect gates, correlated noise or leakage. The decoder assumes independent bit-flip errors and ideal syndrome extraction and correction.

These simplifications make the three-qubit repetition code a useful starting point for studying syndrome decoding and logical error suppression, but the results should not be interpreted as a demonstration of full fault-tolerant quantum computation.

## Technologies

Python · NumPy · Matplotlib · pytest · Monte Carlo simulation · Statistical uncertainty analysis · Quantum error correction
