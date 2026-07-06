import { useState, useEffect } from "react";
import { getHistorical, getRecommendations } from "./api";
import TrafficChart from "./components/TrafficChart";
import RecommendationTable from "./components/RecommendationTable";
import ControlPanel from "./components/ControlPanel";
import MetricsCards from "./components/MetricsCards";

export default function App() {
  const [historical, setHistorical] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [params, setParams] = useState({
    capacity: 1000,
    scale_up_threshold: 0.75,
    scale_down_threshold: 0.35,
    hours_ahead: 24,
  });

  useEffect(() => {
    getHistorical(168).then(setHistorical);
  }, []);

  useEffect(() => {
    setLoading(true);
    getRecommendations(params)
      .then(setRecommendations)
      .finally(() => setLoading(false));
  }, [params]);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "24px", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ fontSize: "28px", fontWeight: 700, marginBottom: "4px" }}>
        📡 Network Traffic Forecasting & Scaling Recommender
      </h1>
      <p style={{ color: "#6b7280", marginBottom: "24px" }}>
        ML-powered bandwidth forecasting with proactive scaling recommendations
      </p>

      <ControlPanel params={params} setParams={setParams} />

      <div style={{ margin: "24px 0" }}>
        <MetricsCards recommendations={recommendations} />
      </div>

      <div style={{ background: "white", padding: "16px", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)", marginBottom: "24px" }}>
        {loading ? <p>Loading forecast...</p> : (
          <TrafficChart
            historical={historical}
            recommendations={recommendations}
            capacity={params.capacity}
            scaleUpThreshold={params.scale_up_threshold}
            scaleDownThreshold={params.scale_down_threshold}
          />
        )}
      </div>

      <div style={{ background: "white", padding: "16px", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <h2 style={{ fontSize: "18px", marginBottom: "12px" }}>Scaling Recommendations</h2>
        <RecommendationTable recommendations={recommendations} />
      </div>
    </div>
  );
}