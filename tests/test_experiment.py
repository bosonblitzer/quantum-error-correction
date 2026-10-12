
"""Tests for QEC experiment calculations."""

import pytest

from experiments.run_experiment import (
    run_experiment,
    theoretical_logical_error_rate,
    wilson_interval,
)


@pytest.mark.parametrize(
    ("p", "expected"),
    [
        (0.0, 0.0),
        (0.01, 0.000298),
        (0.05, 0.00725),
        (0.10, 0.028),
        (0.20, 0.104),
        (0.50, 0.5),
        (1.0, 1.0),
    ],
)
def test_theoretical_logical_error_rate(p, expected):
    assert theoretical_logical_error_rate(p) == pytest.approx(expected)


def test_theoretical_rate_is_below_physical_rate_for_p_between_zero_and_half():
    for p in (0.01, 0.05, 0.10, 0.20, 0.40):
        assert theoretical_logical_error_rate(p) < p


def test_wilson_interval_contains_observed_proportion():
    lower, upper = wilson_interval(100, 1000)

    assert lower < 0.1 < upper


def test_wilson_interval_is_bounded_between_zero_and_one():
    lower, upper = wilson_interval(0, 1000)

    assert 0.0 <= lower <= upper <= 1.0


@pytest.mark.parametrize(
    ("successes", "trials"),
    [
        (-1, 100),
        (101, 100),
        (0, 0),
    ],
)
def test_wilson_interval_rejects_invalid_counts(successes, trials):
    with pytest.raises(ValueError):
        wilson_interval(successes, trials)


def test_experiment_is_reproducible_with_same_seed():
    first = run_experiment([0.05, 0.10], n_trials=1000, seed=123)
    second = run_experiment([0.05, 0.10], n_trials=1000, seed=123)

    assert first == second


def test_simulated_physical_rate_is_reasonable():
    results = run_experiment([0.10], n_trials=20_000, seed=42)

    assert results[0]["physical_error_rate"] == pytest.approx(
        0.10, abs=0.005
    )

def test_repetition_code_suppresses_logical_errors():
    results = run_experiment(
        [0.05],
        n_trials=20_000,
        seed=2026,
    )

    result = results[0]

    assert (
        result["logical_error_rate"]
        < result["physical_error_rate"]
    )
    assert (
        result["logical_error_rate"]
        < result["theoretical_logical_error_rate"] + 0.003
    )
