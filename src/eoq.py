import pandas as pd
import math

# Load inventory data
inventory = pd.read_csv("data/inventory.csv")

# EOQ formula
def calculate_eoq(demand, ordering_cost, holding_cost):
    eoq = math.sqrt((2 * demand * ordering_cost) / holding_cost)
    return round(eoq, 2)


# Calculate EOQ for every product
inventory["EOQ"] = inventory.apply(
    lambda row: calculate_eoq(
        row["annual_demand"],
        row["ordering_cost"],
        row["holding_cost"]
    ),
    axis=1
)

print("\n========== EOQ ANALYSIS ==========")
print(inventory[
    ["product", "annual_demand", "ordering_cost", "holding_cost", "EOQ"]
].to_string(index=False))

print("\n===================================")