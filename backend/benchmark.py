import time
import math
import numpy as np
import random


def monte_carlo_pure_python(S0, r, sigma, T, steps, simulations, seed=42):
    random.seed(seed)
    dt = T / steps
    drift = (r - 0.5 * sigma ** 2) * dt
    vol = sigma * math.sqrt(dt)

    results = []
    for _ in range(simulations):
        price = S0
        for _ in range(steps):
            price *= math.exp(drift + vol * random.gauss(0, 1))
        results.append(price)
    return results


def monte_carlo_numpy(S0, r, sigma, T, steps, simulations, seed=42):
    np.random.seed(seed)
    dt = T / steps
    drift = (r - 0.5 * sigma ** 2) * dt
    vol = sigma * np.sqrt(dt)

    # Full matrix vectorization
    Z = np.random.normal(0, 1, (simulations, steps))
    returns = np.exp(drift + vol * Z)
    price_paths = S0 * np.cumprod(returns, axis=1)
    return price_paths[:, -1]


if __name__ == "__main__":
    S0, r, sigma, T, steps, sims = 100, 0.05, 0.2, 1.0, 252, 100_000

    print("Running benchmark (100,000 simulations, 252 steps)...")

    # Pure Python
    start = time.perf_counter()
    _ = monte_carlo_pure_python(S0, r, sigma, T, steps, sims)
    t_python = time.perf_counter() - start

    # Numpy Vectorized
    start = time.perf_counter()
    _ = monte_carlo_numpy(S0, r, sigma, T, steps, sims)
    t_numpy = time.perf_counter() - start

    print(f"\n Benchmark Results:")
    print(f"Pure Python (loop): {t_python:.4f} seconds")
    print(f"Numpy Vectorized: {t_numpy:.4f} seconds")
    print(f"Speedup: {t_python / t_numpy:.2f}x")
