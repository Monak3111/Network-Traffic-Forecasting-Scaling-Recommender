export default function ControlPanel({ params, setParams }) {
  const update = (key, value) => setParams(prev => ({ ...prev, [key]: value }));

  return (
    <div style={{ display: "flex", gap: "24px", flexWrap: "wrap", padding: "16px", background: "#f9fafb", borderRadius: "8px" }}>
      <div>
        <label>Capacity (Mbps): {params.capacity}</label><br />
        <input type="range" min="500" max="2000" step="50" value={params.capacity}
          onChange={e => update("capacity", Number(e.target.value))} />
      </div>
      <div>
        <label>Scale-Up Threshold: {(params.scale_up_threshold * 100).toFixed(0)}%</label><br />
        <input type="range" min="0.5" max="0.95" step="0.05" value={params.scale_up_threshold}
          onChange={e => update("scale_up_threshold", Number(e.target.value))} />
      </div>
      <div>
        <label>Scale-Down Threshold: {(params.scale_down_threshold * 100).toFixed(0)}%</label><br />
        <input type="range" min="0.1" max="0.5" step="0.05" value={params.scale_down_threshold}
          onChange={e => update("scale_down_threshold", Number(e.target.value))} />
      </div>
      <div>
        <label>Forecast Horizon (hrs): {params.hours_ahead}</label><br />
        <input type="range" min="6" max="72" step="6" value={params.hours_ahead}
          onChange={e => update("hours_ahead", Number(e.target.value))} />
      </div>
    </div>
  );
}

