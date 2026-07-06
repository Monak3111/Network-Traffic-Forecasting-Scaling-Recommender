from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from forecasting import forecast_next_hours, get_historical
from scaling_recommender import recommend_scaling

app = FastAPI(
    title="Network Traffic Forecasting API",
    description="Forecasts bandwidth utilization and recommends scaling actions",
    version="1.0.0"
)

# Allow frontend (React, running on a different port/domain) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your actual frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Network Traffic Forecasting API is running"}

@app.get("/api/historical")
def historical(hours: int = Query(168, ge=1, le=720)):
    return get_historical(hours)

@app.get("/api/forecast")
def forecast(hours_ahead: int = Query(24, ge=1, le=168)):
    return forecast_next_hours(hours_ahead)

@app.get("/api/recommendations")
def recommendations(
    hours_ahead: int = Query(24, ge=1, le=168),
    capacity: float = Query(1000, gt=0),
    scale_up_threshold: float = Query(0.75, gt=0, lt=1),
    scale_down_threshold: float = Query(0.35, gt=0, lt=1),
):
    preds = forecast_next_hours(hours_ahead)
    recs = recommend_scaling(preds, capacity, scale_up_threshold, scale_down_threshold)
    return recs