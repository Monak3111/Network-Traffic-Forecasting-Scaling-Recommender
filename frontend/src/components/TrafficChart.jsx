import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer } from "recharts";

export default function TrafficChart({ historical, recommendations, capacity, scaleUpThreshold, scaleDownThreshold }) {
  const historicalFormatted = historical.map(d => ({
    time: new Date(d.timestamp).toLocaleString(),
    actual: d.bandwidth_mbps,
  }));

  const forecastFormatted = recommendations.map(d => ({
    time: new Date(d.timestamp).toLocaleString(),
    predicted: d.predicted_mbps,
  }));

  const combined = [...historicalFormatted, ...forecastFormatted];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={combined}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" tick={{ fontSize: 10 }} interval={Math.floor(combined.length / 8)} />
        <YAxis label={{ value: "Mbps", angle: -90, position: "insideLeft" }} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="actual" stroke="#6b7280" dot={false} name="Actual" />
        <Line type="monotone" dataKey="predicted" stroke="#2563eb" dot={false} name="Predicted" strokeWidth={2} />
        <ReferenceLine y={capacity * scaleUpThreshold} stroke="red" strokeDasharray="4 4" label="Scale-Up Threshold" />
        <ReferenceLine y={capacity * scaleDownThreshold} stroke="green" strokeDasharray="4 4" label="Scale-Down Threshold" />
      </LineChart>
    </ResponsiveContainer>
  );
}


