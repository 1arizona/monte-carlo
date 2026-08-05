import pytest
import numpy as np
from benchmark import monte_carlo_numpy


def test_random_seed_reproducibility():
    """Test that constant seed gives deterministic results."""
    S0, r, sigma, T, steps, sims = 100, 0.05, 0.2, 1.0, 252, 1000

    run1 = monte_carlo_numpy(S0, r, sigma, T, steps, sims, seed=42)
    run2 = monte_carlo_numpy(S0, r, sigma, T, steps, sims, seed=42)

    np.testing.assert_array_equal(
        run1, run2)


def test_gbm_theoretical_convergence():
    """Test that convergence of averege of Monte Carlo simulations approaches the theoretical expected value - E[S_T] = S0 * exp(r * T)"""
    S0, r, sigma, T, steps, simulations = 100, 0.05, 0.2, 1.0, 252, 100_000

    simulated_prices = monte_carlo_numpy(
        S0, r, sigma, T, steps, simulations, seed=42)
    simulated_mean = np.mean(simulated_prices)

    theoretical_mean = S0 * np.exp(r * T)

    """Deviation of averege of theoretical should be less than 0.5%"""
    assert np.isclose(simulated_mean, theoretical_mean, rtol=5e-3)
