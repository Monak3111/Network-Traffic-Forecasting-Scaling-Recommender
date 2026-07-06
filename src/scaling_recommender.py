import pandas as pd

def recommend_scaling(forecast_df, capacity_mbps=1000, scale_up_threshold=0.75, scale_down_threshold=0.35):
    """
    Given predicted bandwidth and current capacity, recommend scaling actions.

    scale_up_threshold: if predicted load > this % of capacity, recommend scale up
    scale_down_threshold: if predicted load < this % of capacity, recommend scale down
    """
    df = forecast_df.copy()
    df["capacity_mbps"] = capacity_mbps
    df["utilization_pct"] = df["predicted"] / capacity_mbps

    def decide(util):
        if util >= scale_up_threshold:
            return "SCALE UP"
        elif util <= scale_down_threshold:
            return "SCALE DOWN"
        else:
            return "MAINTAIN"

    df["recommendation"] = df["utilization_pct"].apply(decide)
    return df

if __name__ == "__main__":
    forecast = pd.read_csv("xgboost_forecast.csv", parse_dates=["timestamp"])
    recs = recommend_scaling(forecast, capacity_mbps=1000)

    print(recs[["timestamp", "predicted", "utilization_pct", "recommendation"]].tail(20))

    # Summary
    print("\nRecommendation breakdown:")
    print(recs["recommendation"].value_counts())

    recs.to_csv("scaling_recommendations.csv", index=False)