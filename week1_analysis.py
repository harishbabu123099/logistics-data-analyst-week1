import pandas as pd

df = pd.read_csv("logistics_data.csv")

date_cols = ["Order_Date", "Dispatch_Date", "Expected_Delivery_Date", "Actual_Delivery_Date"]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

df["Delivery_Days"] = (df["Actual_Delivery_Date"] - df["Dispatch_Date"]).dt.days
df["Delay_Days"] = (df["Actual_Delivery_Date"] - df["Expected_Delivery_Date"]).dt.days
df["On_Time"] = df["Delay_Days"] <= 0

on_time_rate = df["On_Time"].mean() * 100
avg_delivery_days = df["Delivery_Days"].mean()
cost_per_order = df["Transport_Cost"].sum() / df["Order_ID"].nunique()

print(f"On-time delivery rate: {on_time_rate:.2f}%")
print(f"Average delivery days: {avg_delivery_days:.2f}")
print(f"Transport cost per order: {cost_per_order:.2f}")

route_summary = (
    df.groupby("Destination")
      .agg(
          Orders=("Order_ID", "nunique"),
          Avg_Delivery_Days=("Delivery_Days", "mean"),
          Avg_Cost=("Transport_Cost", "mean"),
          On_Time_Rate=("On_Time", "mean")
      )
      .reset_index()
)

route_summary["On_Time_Rate"] *= 100
print("\nDestination performance:")
print(route_summary)
