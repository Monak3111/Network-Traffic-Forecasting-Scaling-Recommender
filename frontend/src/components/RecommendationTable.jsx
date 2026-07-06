export default function RecommendationTable({ recommendations }) {
  const badgeColor = (action) => {
    if (action === "SCALE UP") return "#fee2e2 text-red-700";
    if (action === "SCALE DOWN") return "#dcfce7 text-green-700";
    return "#f3f4f6 text-gray-700";
  };

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "2px solid #e5e7eb" }}>
            <th style={{ padding: "8px" }}>Time</th>
            <th style={{ padding: "8px" }}>Predicted (Mbps)</th>
            <th style={{ padding: "8px" }}>Utilization</th>
            <th style={{ padding: "8px" }}>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {recommendations.map((r, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #f3f4f6" }}>
              <td style={{ padding: "8px" }}>{new Date(r.timestamp).toLocaleString()}</td>
              <td style={{ padding: "8px" }}>{r.predicted_mbps.toFixed(1)}</td>
              <td style={{ padding: "8px" }}>{r.utilization_pct}%</td>
              <td style={{ padding: "8px" }}>
                <span style={{
                  padding: "2px 8px",
                  borderRadius: "9999px",
                  fontWeight: 600,
                  backgroundColor: r.recommendation === "SCALE UP" ? "#fee2e2" :
                                   r.recommendation === "SCALE DOWN" ? "#dcfce7" : "#f3f4f6",
                  color: r.recommendation === "SCALE UP" ? "#b91c1c" :
                         r.recommendation === "SCALE DOWN" ? "#15803d" : "#374151"
                }}>
                  {r.recommendation}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}