from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from monte_carlo import MultiAssetRequest, MultiAssetResponse, run_multi_asset_monte_carlo

app = FastAPI(
    title="Monte Carlo Portfolio API",
    description="API for simulating multi-asset portfolio with correlated matrix using Monte Carlo method",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "online", "service": "Monte Carlo Engine"}


@app.post("/api/simulate", response_model=MultiAssetResponse)
def simulate_portfolio(request: MultiAssetRequest):
    return run_multi_asset_monte_carlo(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
