import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import pickle

df = pd.read_csv("traffic_data.csv", parse_dates=["timestamp"])
df = df.set_index("timestamp")

def create_features(df):
    df = df.copy()
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek
    df["day_of_month"] = df.index.day
    df["month"] = df.index.month
    df["is_weekend"] = (df.index.dayofweek >= 5).astype(int)

    # Lag features: past values help predict future ones
    for lag in [1, 2, 3, 24, 48, 168]:  # 1-3 hrs ago, 1-2 days ago, 1 week ago
        df[f"lag_{lag}"] = df["bandwidth_mbps"].shift(lag)

    # Rolling stats
    df["rolling_mean_24"] = df["bandwidth_mbps"].shift(1).rolling(24).mean()
    df["rolling_std_24"] = df["bandwidth_mbps"].shift(1).rolling(24).std()

    return df

df_feat = create_features(df).dropna()

FEATURES = [c for c in df_feat.columns if c != "bandwidth_mbps"]
TARGET = "bandwidth_mbps"

# Train/test split (last 7 days as test)
test_hours = 24 * 7
train = df_feat.iloc[:-test_hours]
test = df_feat.iloc[-test_hours:]

X_train, y_train = train[FEATURES], train[TARGET]
X_test, y_test = test[FEATURES], test[TARGET]

model = xgb.XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    early_stopping_rounds=30,
    eval_metric="mae",
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
mape = mean_absolute_percentage_error(y_test, preds) * 100

print(f"XGBoost MAE: {mae:.2f} Mbps")
print(f"XGBoost MAPE: {mape:.2f}%")

# Feature importance
importance = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
print("\nTop features:\n", importance.head(10))

# Save
with open("xgboost_model.pkl", "wb") as f:
    pickle.dump(model, f)

results = test.copy()
results["predicted"] = preds
results.to_csv("xgboost_forecast.csv")