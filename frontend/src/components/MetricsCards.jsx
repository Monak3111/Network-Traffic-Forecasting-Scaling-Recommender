export default function MetricsCards({ recommendations }) {
  const avgUtil = recommendations.length
    ? (recommendations.reduce((a, r) => a + r.utilization_pct, 0) / recommendations.length).toFixed(1)
    : 0;
  const scaleUps = recommendations.filter(r => r.recommendation === "SCALE UP").length;
  const scaleDowns = recommendations.filter(r => r.recommendation === "SCALE DOWN").length;

  const cardStyle = { flex: 1, padding: "16px", background: "white", borderRadius: "8px", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" };

  return (
    <div style={{ display: "flex", gap: "16px", marginBottom: "16px" }}>
      <div style={cardStyle}>
        <div style={{ fontSize: "12px", color: "#6b7280" }}>Avg Utilization</div>
        <div style={{ fontSize: "24px", fontWeight: 700 }}>{avgUtil}%</div>
      </div>
      <div style={cardStyle}>
        <div style={{ fontSize: "12px", color: "#6b7280" }}>Scale-Up Events</div>
        <div style={{ fontSize: "24px", fontWeight: 700, color: "#dc2626" }}>{scaleUps}</div>
      </div>
      <div style={cardStyle}>
        <div style={{ fontSize: "12px", color: "#6b7280" }}>Scale-Down Events</div>
        <div style={{ fontSize: "24px", fontWeight: 700, color: "#16a34a" }}>{scaleDowns}</div>
      </div>
    </div>
  );
}


