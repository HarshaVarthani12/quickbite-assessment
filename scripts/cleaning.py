
import pandas as pd

file = "data/QuickBite_Assessment.xlsx"

orders = pd.read_excel(file, sheet_name="orders")
customers = pd.read_excel(file, sheet_name="customers")
restaurants = pd.read_excel(file, sheet_name="restaurants")
areas = pd.read_excel(file, sheet_name="areas")
partners = pd.read_excel(file, sheet_name="delivery_partners")
feedback = pd.read_excel(file, sheet_name="feedback")

print("Orders:", orders.shape)
print("Customers:", customers.shape)
print("Restaurants:", restaurants.shape)
print("Areas:", areas.shape)
print("Delivery Partners:", partners.shape)
print("Feedback:", feedback.shape)



# Remove duplicate rows
orders = orders.drop_duplicates()
customers = customers.drop_duplicates()
restaurants = restaurants.drop_duplicates()
areas = areas.drop_duplicates()
partners = partners.drop_duplicates()
feedback = feedback.drop_duplicates()

print("Duplicates removed successfully")



# Remove rows with missing mandatory values
orders = orders.dropna(subset=[
    "order_id", "customer_id", "restaurant_id",
    "order_datetime", "order_amount",
    "payment_mode", "order_status"
])

customers = customers.dropna(subset=[
    "customer_id", "customer_name"
])

restaurants = restaurants.dropna(subset=[
    "restaurant_id", "restaurant_name", "area_id", "cuisine"
])

areas = areas.dropna(subset=[
    "area_id", "area_name", "city"
])

partners = partners.dropna(subset=[
    "partner_id", "partner_name", "vehicle_type"
])

feedback = feedback.dropna(subset=[
    "feedback_id", "order_id", "rating"
])

print("Missing mandatory values removed")



# Remove extra spaces from text columns
tables = [orders, customers, restaurants, areas, partners, feedback]

for df in tables:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

print("Extra spaces removed")



# Clean city names
areas["city"] = areas["city"].str.title()
areas["city"] = areas["city"].replace({
    "Blr": "Bengaluru",
    "Hyd": "Hyderabad",
    "Madras": "Chennai"
})

# Clean cuisine names
restaurants["cuisine"] = restaurants["cuisine"].str.title()
restaurants["cuisine"] = restaurants["cuisine"].replace({
    "Biriyani": "Biryani",
    "Dessert": "Desserts",
    "Italian - Pizza": "Pizza",
    "N. Indian": "North Indian",
    "North-Indian": "North Indian",
    "South-Indian": "South Indian"
})

# Clean vehicle types
partners["vehicle_type"] = partners["vehicle_type"].str.title()
partners["vehicle_type"] = partners["vehicle_type"].replace({
    "Bike": "Motorbike",
    "Motor Bike": "Motorbike",
    "Activa": "Scooter",
    "Scooty": "Scooter",
    "Cycle": "Bicycle",
    "Ev": "Electric Scooter",
    "Ev Scooter": "Electric Scooter",
    "E-Scooter": "Electric Scooter"
})

# Clean order status
orders["order_status"] = orders["order_status"].str.title()
orders["order_status"] = orders["order_status"].replace({
    "Completed": "Delivered",
    "Canceled": "Cancelled"
})

# Clean payment modes
orders["payment_mode"] = orders["payment_mode"].str.upper()
orders["payment_mode"] = orders["payment_mode"].replace({
    "CASH": "CASH ON DELIVERY",
    "COD": "CASH ON DELIVERY",
    "GPAY": "UPI",
    "PHONEPE": "UPI",
    "CREDIT CARD": "CARD",
    "DEBIT CARD": "CARD",
    "PAYTM WALLET": "WALLET",
    "AMAZON PAY": "WALLET"
})

# Clean names and coupon codes
customers["customer_name"] = customers["customer_name"].str.title()
restaurants["restaurant_name"] = restaurants["restaurant_name"].str.title()
partners["partner_name"] = partners["partner_name"].str.title()
orders["coupon_code"] = orders["coupon_code"].str.upper()

print("Inconsistent values standardised")


# Standardise date and time formats
orders["order_datetime"] = pd.to_datetime(
    orders["order_datetime"], format="mixed",
    dayfirst=True, errors="coerce"
)

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"], format="mixed",
    dayfirst=True, errors="coerce"
).dt.date

restaurants["onboard_date"] = pd.to_datetime(
    restaurants["onboard_date"], format="mixed",
    dayfirst=True, errors="coerce"
).dt.date

partners["join_date"] = pd.to_datetime(
    partners["join_date"], format="mixed",
    dayfirst=True, errors="coerce"
).dt.date

feedback["feedback_date"] = pd.to_datetime(
    feedback["feedback_date"], format="mixed",
    dayfirst=True, errors="coerce"
).dt.date

print("Date formats cleaned")



# Clean order amount
orders["order_amount"] = orders["order_amount"].astype(str)
orders["order_amount"] = orders["order_amount"].str.replace(
    r"(?i)Rs\.?|INR|₹|,|\s", "", regex=True
)
orders["order_amount"] = pd.to_numeric(
    orders["order_amount"], errors="coerce"
)

# Clean delivery minutes
orders["delivery_minutes"] = orders["delivery_minutes"].astype(str)
orders["delivery_minutes"] = orders["delivery_minutes"].str.replace(
    r"(?i)mins?|m|\s", "", regex=True
)
orders["delivery_minutes"] = pd.to_numeric(
    orders["delivery_minutes"], errors="coerce"
)

orders = orders.dropna(subset=["order_datetime", "order_amount"])

print("Numerical values cleaned")



# Standardise phone numbers
for df in [customers, partners]:
    df["phone"] = df["phone"].astype("string")
    df["phone"] = df["phone"].str.replace(
        r"\D", "", regex=True
    ).str[-10:]

# Standardise email addresses
customers["email"] = customers["email"].str.lower().str.strip()

print("Phone numbers and emails cleaned")



# Remove duplicates after standardisation
orders = orders.drop_duplicates()
customers = customers.drop_duplicates()
restaurants = restaurants.drop_duplicates()
areas = areas.drop_duplicates()
partners = partners.drop_duplicates()
feedback = feedback.drop_duplicates()

# Save all cleaned tables
with pd.ExcelWriter(
    "cleaned_data/Quick_Bite_Data_Cleaning.xlsx",
    engine="openpyxl"
) as writer:

    orders.to_excel(writer, sheet_name="orders", index=False)
    customers.to_excel(writer, sheet_name="customers", index=False)
    restaurants.to_excel(writer, sheet_name="restaurants", index=False)
    areas.to_excel(writer, sheet_name="areas", index=False)
    partners.to_excel(writer, sheet_name="delivery_partners", index=False)
    feedback.to_excel(writer, sheet_name="feedback", index=False)

print("Cleaned Excel file created successfully")



# Task 2 - Combine all cleaned tables

# Make sure each ID is unique
orders = orders.drop_duplicates(subset=["order_id"])
customers = customers.drop_duplicates(subset=["customer_id"])
restaurants = restaurants.drop_duplicates(subset=["restaurant_id"])
areas = areas.drop_duplicates(subset=["area_id"])
partners = partners.drop_duplicates(subset=["partner_id"])
feedback = feedback.drop_duplicates(subset=["order_id"])

# Combine orders with customers
combined = orders.merge(
    customers[["customer_id", "customer_name"]],
    on="customer_id",
    how="left"
)

# Combine with restaurants
combined = combined.merge(
    restaurants[["restaurant_id", "restaurant_name", "cuisine", "area_id"]],
    on="restaurant_id",
    how="left"
)

# Combine with areas
combined = combined.merge(
    areas[["area_id", "area_name", "city"]],
    on="area_id",
    how="left"
)

# Combine with delivery partners
combined = combined.merge(
    partners[["partner_id", "partner_name", "vehicle_type"]],
    on="partner_id",
    how="left"
)

# Combine with customer feedback
combined = combined.merge(
    feedback[["order_id", "rating", "comment"]],
    on="order_id",
    how="left"
)

# Separate date, time and day
combined["order_date"] = combined["order_datetime"].dt.date
combined["order_time"] = combined["order_datetime"].dt.strftime("%H:%M:%S")
combined["order_day"] = combined["order_datetime"].dt.day_name()

# Check whether delivery is late
combined["is_late"] = combined["delivery_minutes"] > 45

# Leave late status blank for non-delivered orders
combined["is_late"] = combined["is_late"].astype("boolean")

combined.loc[
    (combined["order_status"] != "Delivered") |
    (combined["delivery_minutes"].isna()),
    "is_late"
] = pd.NA

# Select the required columns
columns = [
    "order_id",
    "order_date",
    "order_time",
    "order_day",
    "customer_name",
    "restaurant_name",
    "cuisine",
    "area_name",
    "city",
    "partner_name",
    "vehicle_type",
    "order_amount",
    "payment_mode",
    "coupon_code",
    "order_status",
    "delivery_minutes",
    "is_late",
    "rating",
    "comment"
]

combined = combined[columns]

# Verify one row per order
assert combined["order_id"].is_unique

# Save the combined dataset
combined.to_excel(
    "cleaned_data/Quick_Bite_Combined_Data.xlsx",
    index=False
)

print("Combined Excel file created successfully")
print("Total orders:", len(combined))
print("Total columns:", len(combined.columns))
