def recommend_scaling(predictions, capacity_mbps=1000, scale_up_threshold=0.75, scale_down_threshold=0.35):
    results = []
    for p in predictions:
        utilization = p["predicted_mbps"] / capacity_mbps
        if utilization >= scale_up_threshold:
            action = "SCALE UP"
        elif utilization <= scale_down_threshold:
            action = "SCALE DOWN"
        else:
            action = "MAINTAIN"

        results.append({
            **p,
            "utilization_pct": round(utilization * 100, 2),
            "recommendation": action
        })
    return results