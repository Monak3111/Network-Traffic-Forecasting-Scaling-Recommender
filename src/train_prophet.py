import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import pickle

df = pd.read_csv("traffic_data.csv", parse_dates=["timestamp"])

# Prophet requires columns named 'ds' and 'y'
prophet_df = df.rename(columns={"timestamp": "ds", "bandwidth_mbps": "y"})

# Train/test split (last 7 days as test)
test_hours = 24 * 7
train_df = prophet_df.iloc[:-test_hours]
test_df = prophet_df.iloc[-test_hours:]

model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=False,
    changepoint_prior_scale=0.05,  # controls trend flexibility
)
model.fit(train_df)

# Forecast including the test period
future = model.make_future_dataframe(periods=test_hours, freq="h")
forecast = model.predict(future)

# Evaluate on test set
merged = test_df.merge(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds")
mae = (merged["y"] - merged["yhat"]).abs().mean()
mape = ((merged["y"] - merged["yhat"]).abs() / merged["y"]).mean() * 100

print(f"MAE: {mae:.2f} Mbps")
print(f"MAPE: {mape:.2f}%")

# Save model and forecast
with open("prophet_model.pkl", "wb") as f:
    pickle.dump(model, f)

forecast.to_csv("prophet_forecast.csv", index=False)

fig = model.plot(forecast)
fig.savefig("prophet_forecast.png")