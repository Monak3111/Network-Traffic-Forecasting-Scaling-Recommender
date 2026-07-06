import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE });

export const getHistorical = (hours = 168) =>
  api.get(`/api/historical?hours=${hours}`).then(res => res.data);

export const getForecast = (hoursAhead = 24) =>
  api.get(`/api/forecast?hours_ahead=${hoursAhead}`).then(res => res.data);

export const getRecommendations = (params) =>
  api.get("/api/recommendations", { params }).then(res => res.data);