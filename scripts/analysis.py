
import pandas as pd

# Read the combined dataset
df = pd.read_excel("cleaned_data/Quick_Bite_Combined_Data.xlsx")

# Consider only delivered orders
df = df[df["order_status"] == "Delivered"].copy()

df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

print("Total delivered orders:", len(df))

# Task 3.1 - Area Performance

area = df.groupby(["city", "area_name"]).agg(
    total_orders=("order_id", "count"),
    total_revenue=("order_amount", "sum"),
    average_order_amount=("order_amount", "mean"),
    average_delivery_time=("delivery_minutes", "mean"),
    late_deliveries=("is_late", "sum"),
    late_percentage=("is_late", "mean"),
    average_rating=("rating", "mean")
).reset_index()

area["late_percentage"] = area["late_percentage"] * 100

area = area.sort_values(
    "total_revenue", ascending=False
).reset_index(drop=True)

area.insert(0, "rank", area.index + 1)

area = area.round(2)

print("Area Performance completed")


# Task 3.2 - Top Cuisine by Day

cuisine = df.groupby(
    ["order_day", "cuisine"]
).size().reset_index(name="order_count")

daily_orders = df.groupby(
    "order_day"
).size().reset_index(name="total_daily_orders")

cuisine = cuisine.merge(
    daily_orders, on="order_day"
)

cuisine["order_share_percentage"] = (
    cuisine["order_count"] /
    cuisine["total_daily_orders"] * 100
)

# Find the most ordered cuisine for each day
maximum = cuisine.groupby(
    "order_day"
)["order_count"].transform("max")

top_cuisine = cuisine[
    cuisine["order_count"] == maximum
].copy()

days = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

top_cuisine["order_day"] = pd.Categorical(
    top_cuisine["order_day"],
    categories=days,
    ordered=True
)

top_cuisine = top_cuisine.sort_values(
    "order_day"
).reset_index(drop=True)

top_cuisine = top_cuisine.round(2)

print("Top Cuisine by Day completed")


# Vehicle Performance

vehicle = df.groupby("vehicle_type").agg(
    total_deliveries=("order_id", "count"),
    average_delivery_time=("delivery_minutes", "mean"),
    late_deliveries=("is_late", "sum"),
    late_percentage=("is_late", "mean"),
    average_rating=("rating", "mean")
).reset_index()

vehicle["late_percentage"] = (
    vehicle["late_percentage"] * 100
)

vehicle["on_time_percentage"] = (
    100 - vehicle["late_percentage"]
)

vehicle = vehicle.sort_values(
    "average_delivery_time"
).reset_index(drop=True)

vehicle = vehicle.round(2)

print("Vehicle Performance completed")




with pd.ExcelWriter(
    "analysis/Quick_Bite_Analysis.xlsx",
    engine="openpyxl"
) as writer:

    area.to_excel(
        writer, sheet_name="Area Performance", index=False
    )

    top_cuisine.to_excel(
        writer, sheet_name="Top Cuisine by Day", index=False
    )

    vehicle.to_excel(
        writer, sheet_name="Vehicle Performance", index=False
    )

print("Analysis Excel file created successfully")
