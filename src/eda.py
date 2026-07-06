import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("traffic_data.csv", parse_dates=["timestamp"])

# Plot full time series
plt.figure(figsize=(15, 5))
plt.plot(df["timestamp"], df["bandwidth_mbps"])
plt.title("Network Bandwidth Over Time")
plt.xlabel("Time")
plt.ylabel("Bandwidth (Mbps)")
plt.tight_layout()
plt.savefig("full_series.png")
plt.show()

# Plot a single week to see daily/weekly pattern clearly
week_df = df.iloc[:24*7]
plt.figure(figsize=(15, 5))
plt.plot(week_df["timestamp"], week_df["bandwidth_mbps"])
plt.title("Bandwidth - First Week (Daily/Weekly Pattern)")
plt.xlabel("Time")
plt.ylabel("Bandwidth (Mbps)")
plt.tight_layout()
plt.savefig("week_series.png")
plt.show()

print(df["bandwidth_mbps"].describe())