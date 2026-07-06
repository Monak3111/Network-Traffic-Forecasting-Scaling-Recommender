import pandas as pd
import numpy as np
import pickle
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "xgboost_model.pkl"
DATA_PATH = Path(__file__).parent / "data" / "traffic_data.csv"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def load_historical_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    return df

def create_features(df):
    df = df.copy().set_index("timestamp")
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek
    df["day_of_month"] = df.index.day
    df["month"] = df.index.month
    df["is_weekend"] = (df.index.dayofweek >= 5).astype(int)

    for lag in [1, 2, 3, 24, 48, 168]:
        df[f"lag_{lag}"] = df["bandwidth_mbps"].shift(lag)

    df["rolling_mean_24"] = df["bandwidth_mbps"].shift(1).rolling(24).mean()
    df["rolling_std_24"] = df["bandwidth_mbps"].shift(1).rolling(24).std()

    return df

def forecast_next_hours(hours_ahead=24):
    """
    Iteratively predicts the next N hours using the trained XGBoost model.
    Since we use lag features, we predict one step at a time and feed
    predictions back in as the "actuals" for the next lag calculation.
    """
    df = load_historical_data()
    working_df = df.copy()

    predictions = []
    last_timestamp = working_df["timestamp"].iloc[-1]

    for step in range(hours_ahead):
        feat_df = create_features(working_df).dropna()
        latest_row = feat_df.iloc[[-1]]

        feature_cols = [c for c in feat_df.columns if c != "bandwidth_mbps"]
        pred = model.predict(latest_row[feature_cols])[0]

        next_timestamp = last_timestamp + pd.Timedelta(hours=step + 1)
        predictions.append({"timestamp": next_timestamp, "predicted_mbps": float(pred)})

        # Append prediction to working data so next lag features can use it
        new_row = pd.DataFrame({"timestamp": [next_timestamp], "bandwidth_mbps": [pred]})
        working_df = pd.concat([working_df, new_row], ignore_index=True)

    return predictions

def get_historical(hours=168):
    df = load_historical_data()
    recent = df.tail(hours)
    return recent.to_dict(orient="records")