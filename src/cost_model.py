import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

inventory_file = DATA_FOLDER / "inventory.csv"
ga_file = DATA_FOLDER / "ga_result.csv"

# ==========================================
# CHECK FILES
# ==========================================

if not inventory_file.exists():
    raise FileNotFoundError(
        f"Missing file: {inventory_file}"
    )

if not ga_file.exists():
    raise FileNotFoundError(
        "ga_result.csv not found. "
        "Run genetic_algorithm.py first."
    )

# ==========================================
# LOAD INVENTORY
# ==========================================

inventory = pd.read_csv(
    inventory_file
)

# ==========================================
# EOQ
# ==========================================

inventory["EOQ"] = (
    (
        2
        * inventory["annual_demand"]
        * inventory["ordering_cost"]
    )
    / inventory["holding_cost"]
) ** 0.5

# ==========================================
# COSTS
# ==========================================

inventory["ordering_cost_year"] = (
    inventory["annual_demand"]
    / inventory["EOQ"]
) * inventory["ordering_cost"]

inventory["holding_cost_year"] = (
    inventory["EOQ"] / 2
) * inventory["holding_cost"]

inventory["total_inventory_cost"] = (
    inventory["ordering_cost_year"]
    + inventory["holding_cost_year"]
)

# ==========================================
# DISPLAY INVENTORY COST
# ==========================================

print("\n========== INVENTORY COST ==========")

print(
    inventory[
        [
            "product",
            "annual_demand",
            "EOQ",
            "ordering_cost_year",
            "holding_cost_year",
            "total_inventory_cost"
        ]
    ].round(2).to_string(index=False)
)

total_inventory_cost = (
    inventory[
        "total_inventory_cost"
    ].sum()
)

print("\n=====================================")

print(
    f"Total annual inventory cost: "
    f"₹{total_inventory_cost:.2f}"
)

# ==========================================
# READ FINAL GA RESULT
# ==========================================

ga_result = pd.read_csv(
    ga_file
)

if (
    "transportation_cost"
    not in ga_result.columns
):
    raise ValueError(
        "ga_result.csv must contain "
        "'transportation_cost' column."
    )

if len(ga_result) == 0:
    raise ValueError(
        "ga_result.csv is empty."
    )

transportation_cost = float(
    ga_result.iloc[0][
        "transportation_cost"
    ]
)

# ==========================================
# TOTAL LOGISTICS COST
# ==========================================

total_logistics_cost = (
    total_inventory_cost
    + transportation_cost
)

print(
    f"Transportation cost: "
    f"₹{transportation_cost:.2f}"
)

print(
    f"TOTAL LOGISTICS COST: "
    f"₹{total_logistics_cost:.2f}"
)

# ==========================================
# SAVE COST SUMMARY
# ==========================================

cost_summary = pd.DataFrame({
    "inventory_cost": [
        round(total_inventory_cost, 2)
    ],
    "transportation_cost": [
        round(transportation_cost, 2)
    ],
    "total_logistics_cost": [
        round(total_logistics_cost, 2)
    ]
})

cost_summary.to_csv(
    DATA_FOLDER / "cost_summary.csv",
    index=False
)

print(
    "\nCost summary saved successfully."
)

print("\n=====================================")