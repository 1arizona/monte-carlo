import numpy as np
from pydantic import BaseModel, Field
from typing import List


class AssetConfig(BaseModel):
    name: str = Field(..., description="Name of the asset, e.g., ETF S&P 500")
    weight: float = Field(...,
                          description="Weight of the asset in the portfolio (0.0 to 1.0)")
    annual_return: float = Field(...,
                                 description="Expected annual rate of return")
    annual_volatility: float = Field(...,
                                     description="Annual volatility (standard deviation)")


class MultiAssetRequest(BaseModel):
    initial_capital: float = 100000.0
    years: int = 10
    simulations_count: int = 10000
    monthly_contribution: float = 1000.0
    assets: List[AssetConfig]
    correlation_matrix: List[List[float]]


class YearResult(BaseModel):
    year: int
    p10: float
    p50: float
    p90: float


class MultiAssetResponse(BaseModel):
    results: List[YearResult]
    expected_portfolio_return: float
    expected_portfolio_volatility: float


def run_multi_asset_monte_carlo(req: MultiAssetRequest) -> MultiAssetResponse:
    num_assets = len(req.assets)
    steps_per_year = 12
    total_steps = req.years * steps_per_year
    dt = 1.0 / steps_per_year

    # Weights normalization
    weights = np.array([a.weight for a in req.assets], dtype=np.float64
                       )
    weights /= np.sum(weights)

    returns = np.array([a.annual_return for a in req.assets], dtype=np.float64)
    vols = np.array([a.annual_volatility for a in req.assets],
                    dtype=np.float64)
    corr_matrix = np.array(req.correlation_matrix, dtype=np.float64)

    # Cholesky decomposition for correlated random variables
    L = np.linalg.cholesky(corr_matrix)

    drifts = (returns - 0.5 * (vols ** 2)) * dt
    vols_dt = vols * np.sqrt(dt)

    # Nonlinear generation of correlated random shocks [steps, assets, simulations]
    Z = np.random.normal(0, 1, size=(
        total_steps, num_assets, req.simulations_count))
    correlated_shocks = np.einsum('ij, jkl -> ikl', L, Z)

    asset_paths = np.zeros(
        (total_steps + 1, num_assets, req.simulations_count), dtype=np.float64)
    asset_paths[0] = (req.initial_capital * weights[:, np.newaxis])

    for t in range(1, total_steps + 1):
        prev_prices = asset_paths[t - 1]
        shocks = correlated_shocks[t - 1]
        growth = np.exp(drifts[:, np.newaxis] +
                        vols_dt[:, np.newaxis] * shocks)
        next_prices = prev_prices * growth

        if req.monthly_contribution > 0:
            next_prices += (req.monthly_contribution * weights[:, np.newaxis])

        asset_paths[t] = next_prices

    # Aggregate portfolio value across assets
    portfolio_paths = np.sum(asset_paths, axis=1)

    yearly_results: List[YearResult] = []
    for year in range(req.years + 1):
        step_idx = year * steps_per_year
        vals = portfolio_paths[step_idx]
        yearly_results.append(YearResult(
            year=year,
            p10=round(float(np.percentile(vals, 10)), 2),
            p50=round(float(np.percentile(vals, 50)), 2),
            p90=round(float(np.percentile(vals, 90)), 2)
        ))

    # Calculate metrics for portfolio
    port_return = float(np.dot(weights, returns))
    cov_matrix = np.outer(vols, vols) * corr_matrix
    port_volatility = float(
        np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))

    return MultiAssetResponse(
        results=yearly_results,
        expected_portfolio_return=round(port_return, 4),
        expected_portfolio_volatility=round(port_volatility, 4)
    )
