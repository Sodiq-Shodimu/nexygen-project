from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import statsmodels.api as sm
from contextlib import asynccontextmanager
from pathlib import Path
import pandas as pd
from typing import Literal


models = {}
BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    models["scope1"] = sm.load(str(BASE_DIR / "scope1_model.pkl"))
    models["scope2"] = sm.load(str(BASE_DIR / "scope2_model.pkl"))
    yield
    models.clear()


app = FastAPI(
    title="Nexygen API",
    description="This is an API endpoint that scope 1 and scope 2 emission for nexygen",
    version="0.1.0",
    lifespan=lifespan
)

# define a structure/validation for our request and response model

class ForecastRequest(BaseModel):
    emission_type: Literal['scope1', 'scope2']
    steps: int

class ForecastResponse(BaseModel):
    emission_type: str
    forecast: list[float]
    dates: list[str]

@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "Nexygen Emission Forecast API",
    }

# http://127.0.0.1:8000/predict

# @app.post("/product")
# def forecast_emissions():