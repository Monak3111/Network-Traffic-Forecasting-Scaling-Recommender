import os
import pandas as pd
import numpy as np


def generate_traffic_data(days=180, freq="h"):
    """
    Generates synthetic network bandwidth data with:
    - Daily seasonality (higher during work hours)
    - Weekly seasonality (lower on weekends)
    - Upward trend (organic growth)
    - Random traffic spikes (simulating incidents/events)
    """

    periods = days * 24 if freq == "h" else days
    date_rng = pd.date_range(start="2025-01-01", periods=periods, freq=freq)

    df = pd.DataFrame({"timestamp": date_rng})
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["day_index"] = np.arange(len(df))

    # Base load (Mbps)
    base_load = 500

    # Daily seasonality (active hours ~ 6 AM to 6 PM)
    daily_pattern = np.maximum(
        300 * np.sin((df["hour"] - 6) / 24 * 2 * np.pi),
        0
    )

    # Weekly seasonality (weekend reduction)
    weekend_dampening = np.where(df["day_of_week"] >= 5, 0.6, 1.0)

    # Trend (gradual growth over time)
    trend = df["day_index"] * 0.05

    # Random noise
    noise = np.random.normal(0, 20, size=len(df))

    # Random spikes (rare traffic surges)
    spikes = np.zeros(len(df))
    spike_indices = np.random.choice(
        len(df),
        size=max(1, int(len(df) * 0.01)),
        replace=False
    )
    spikes[spike_indices] = np.random.uniform(200, 600, size=len(spike_indices))

    # Final bandwidth calculation
    df["bandwidth_mbps"] = (
        (base_load + daily_pattern + trend + noise + spikes)
        * weekend_dampening
    ).clip(lower=50)

    return df[["timestamp", "bandwidth_mbps"]]


if __name__ == "__main__":
    df = generate_traffic_data(days=180)
    df.to_csv("traffic_data.csv", index=False)

    print(f"Generated {len(df)} rows of traffic data")
    print(df.head())