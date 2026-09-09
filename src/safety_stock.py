import pandas as pd
import math

# Load data
demand_history = pd.read_csv("data/demand_history.csv")
inventory = pd.read_csv("data/inventory.csv")


# Calculate Safety Stock
def calculate_safety_stock(product_data, lead_time):
    demand_std = product_data["demand"].std()

    safety_stock = demand_std * math.sqrt(lead_time)

    return round(safety_stock, 2)


# Calculate for each product
results = []

for _, product in inventory.iterrows():

    product_name = product["product"]
    lead_time = product["lead_time"]

    product_data = demand_history[
        demand_history["product"] == product_name
    ]

    safety_stock = calculate_safety_stock(
        product_data,
        lead_time
    )

    results.append({
        "product": product_name,
        "lead_time": lead_time,
        "daily_demand": product["daily_demand"],
        "safety_stock": safety_stock
    })


# Convert results to DataFrame
result_df = pd.DataFrame(results)


print("\n========== SAFETY STOCK ANALYSIS ==========")

print(
    result_df.to_string(index=False)
)

print("\n===========================================")