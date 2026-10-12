# Monte Carlo Evaluation of a Three-Qubit Repetition Code

## Abstract

This project investigates how independent physical bit-flip errors affect the logical error probability of a three-qubit repetition code. A Python simulation samples physical errors, calculates error syndromes, applies a minimum-weight correction, and estimates the resulting logical error rate. Monte Carlo estimates are compared with an analytical prediction, with Wilson 95% confidence intervals used to quantify statistical uncertainty.

For a physical bit-flip probability of 10%, the simulation estimates a logical error rate of 2.742%, compared with a theoretical prediction of 2.800%. At a physical error probability of 20%, the simulated logical error rate is 10.633%, compared with 10.400% predicted theoretically. These results illustrate the error-suppression capability of the repetition code under the assumptions of the model.

## 1. Research Question

How does the physical bit-flip probability affect the logical error rate of a three-qubit repetition code using syndrome-based decoding?

## 2. Theoretical Background

The logical computational basis is encoded as

$$
|0_L\rangle = |000\rangle,\qquad |1_L\rangle = |111\rangle.
$$
The code protects against independent bit-flip errors by encoding one logical bit across three physical qubits. The two parity checks are

$$
s_1 = e_1 \oplus e_2,\qquad s_2 = e_2 \oplus e_3,
$$

where $e_i \in \{0,1\}$ indicates whether physical qubit $i$ experienced a bit flip, and $\oplus$ denotes exclusive OR.

The decoder identifies the most likely single-qubit error consistent with the observed syndrome, assuming independent bit flips with probability \(p<0.5\).

A logical error occurs when at least two of the three physical qubits experience bit flips. The probability of this event is

$$
\begin{aligned}
P_L &= \binom{3}{2}p^2(1-p)+p^3\\
    &= 3p^2-2p^3.
\end{aligned}
$$

For \(0<p<0.5\), this theoretical logical error probability is lower than the physical error probability \(p\).

## 3. Methodology

The simulation uses Python and NumPy to generate independent bit-flip error patterns. For each trial, it calculates the syndrome, applies the decoder's correction, and checks whether the residual error corresponds to a logical bit flip.

Six physical error probabilities are investigated: 0.01, 0.03, 0.05, 0.10, 0.15 and 0.20. Each probability is evaluated over 100,000 Monte Carlo trials using a fixed random seed to support reproducibility.

The estimated logical error rate is the number of logical failures divided by the number of trials. A Wilson 95% confidence interval is calculated for each estimate. Results, including theoretical predictions and error-reduction metrics, are exported to CSV. A plotting script visualises the simulated and theoretical error rates alongside the uncorrected physical error-rate baseline.

## 4. Results
![Simulated and theoretical logical error rates](results/logical_error_comparison.png)
At a physical error probability of 0.10, the simulated logical error rate is 0.02742, compared with a theoretical prediction of 0.02800. The simulation therefore estimates a reduction in error probability of approximately 72.6% relative to the measured physical error rate.

At a physical error probability of 0.15, the simulated logical error rate is 0.06103, compared with a theoretical value of 0.06075. The estimated relative error reduction is approximately 59.3%.

At a physical error probability of 0.20, the simulated logical error rate is 0.10633, compared with a theoretical value of 0.10400. The estimated relative error reduction is approximately 47.0%. The theoretical prediction falls slightly below the simulation's Wilson 95% confidence interval at this point, so the discrepancy warrants further investigation rather than being dismissed.

Overall, the results indicate that the relative benefit of this repetition-code decoder decreases as the physical error probability increases across the tested range.

## 5. Limitations

This is a classical error-pattern simulation of a simplified quantum error-correction code, not a full quantum-state or quantum-circuit simulation. It models independent bit-flip errors only. It does not include phase-flip errors, correlated noise, faulty syndrome measurements, imperfect gates, leakage, or the overhead of implementing correction on quantum hardware.

The simulation therefore demonstrates a limited theoretical principle rather than the performance of a practical fault-tolerant quantum computer. The confidence intervals quantify sampling uncertainty under the simulated model; they do not account for model assumptions or implementation errors.

## 6. Conclusion

The simulation compares Monte Carlo estimates with the analytical logical-error probability of a three-qubit repetition code. The results demonstrate error suppression under independent bit-flip noise for the tested physical error probabilities, while showing that the relative benefit declines as the physical error probability increases.

The project provides a reproducible foundation for further work on decoder evaluation, alternative noise models, and the effect of imperfect syndrome measurements.
