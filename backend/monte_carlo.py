import numpy as np
from pydantic import BaseModel
from typing import List


class SingleAssetRequest(BaseModel):
    initial_capital: float = 20000.0
    annual_return: float = 0.08
    annual_volatility: float = 0.15
    years: int = 15
    simulations_count: int = 10000
    monthly_contribution: float = 500.0


class YearResult(BaseModel):
    year: int
    p10: float
    p50: float
    p90: float


def run_single_asset_simulation(params: SingleAssetRequest) -> List[YearResult]:
    steps_per_year = 12
    total_steps = params.years * steps_per_year
    dt = 1.0 / steps_per_year

    drift = (params.annual_return - 0.5 * (params.annual_volatility ** 2)) * dt
    vol = params.annual_volatility * np.sqrt(dt)

    random_shocks = np.random.normal(
        0, 1, size=(total_steps, params.simulations_count))
    portfolio_paths = np.zeros((total_steps + 1, params.simulations_count))
    portfolio_paths[0] = params.initial_capital

    for t in range(1, total_steps + 1):
        prev_val = portfolio_paths[t - 1]
        z = random_shocks[t - 1]
        portfolio_paths[t] = prev_val * \
            np.exp(drift + vol * z) + params.monthly_contribution

    results = []
    for year in range(params.years + 1):
        step_idx = year * steps_per_year
        vals = portfolio_paths[step_idx]
        results.append(YearResult(
            year=year,
            p10=round(float(np.percentile(vals, 10)), 2),
            p50=round(float(np.percentile(vals, 50)), 2),
            p90=round(float(np.percentile(vals, 90)), 2)
        ))

    return results
