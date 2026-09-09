import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

inventory_file = DATA_FOLDER / "inventory.csv"
cost_file = DATA_FOLDER / "cost_summary.csv"

if not inventory_file.exists():
    raise FileNotFoundError(
        "inventory.csv not found."
    )

if not cost_file.exists():
    raise FileNotFoundError(
        "cost_summary.csv not found. "
        "Run cost_model.py first."
    )

inventory = pd.read_csv(
    inventory_file
)

cost_summary = pd.read_csv(
    cost_file
)

base_inventory_cost = float(
    cost_summary.loc[
        0,
        "inventory_cost"
    ]
)

base_transportation_cost = float(
    cost_summary.loc[
        0,
        "transportation_cost"
    ]
)

# ==========================================
# INVENTORY COST FUNCTION
# ==========================================

def calculate_inventory_cost(data):

    data = data.copy()

    data["EOQ"] = (
        (
            2
            * data["annual_demand"]
            * data["ordering_cost"]
        )
        / data["holding_cost"]
    ) ** 0.5

    data["ordering_cost_year"] = (
        data["annual_demand"]
        / data["EOQ"]
    ) * data["ordering_cost"]

    data["holding_cost_year"] = (
        data["EOQ"] / 2
    ) * data["holding_cost"]

    data["total_inventory_cost"] = (
        data["ordering_cost_year"]
        + data["holding_cost_year"]
    )

    return data[
        "total_inventory_cost"
    ].sum()


# ==========================================
# BASE
# ==========================================

base_total = (
    base_inventory_cost
    + base_transportation_cost
)

# ==========================================
# DEMAND +10%
# ==========================================

demand_plus = inventory.copy()

demand_plus["annual_demand"] *= 1.10

inventory_plus = calculate_inventory_cost(
    demand_plus
)

transport_plus = (
    base_transportation_cost * 1.10
)

total_plus = (
    inventory_plus
    + transport_plus
)

# ==========================================
# TRANSPORTATION +20%
# ==========================================

transport_20 = (
    base_transportation_cost * 1.20
)

total_20 = (
    base_inventory_cost
    + transport_20
)

# ==========================================
# DEMAND -10%
# ==========================================

demand_minus = inventory.copy()

demand_minus["annual_demand"] *= 0.90

inventory_minus = calculate_inventory_cost(
    demand_minus
)

transport_minus = (
    base_transportation_cost * 0.90
)

total_minus = (
    inventory_minus
    + transport_minus
)

# ==========================================
# CREATE RESULT
# ==========================================

scenario_data = pd.DataFrame({

    "scenario": [
        "Base Scenario",
        "Demand +10%",
        "Transportation Cost +20%",
        "Demand -10%"
    ],

    "inventory_cost": [
        base_inventory_cost,
        inventory_plus,
        base_inventory_cost,
        inventory_minus
    ],

    "transportation_cost": [
        base_transportation_cost,
        transport_plus,
        transport_20,
        transport_minus
    ],

    "total_cost": [
        base_total,
        total_plus,
        total_20,
        total_minus
    ]
})

scenario_data = scenario_data.round(2)

# ==========================================
# DISPLAY
# ==========================================

print("\n========== SCENARIO ANALYSIS ==========")

for _, row in scenario_data.iterrows():

    print(f"\n{row['scenario']}")

    print(
        f"Inventory Cost: "
        f"₹{row['inventory_cost']:.2f}"
    )

    print(
        f"Transportation Cost: "
        f"₹{row['transportation_cost']:.2f}"
    )

    print(
        f"Total Cost: "
        f"₹{row['total_cost']:.2f}"
    )

# ==========================================
# SAVE
# ==========================================

scenario_data.to_csv(
    DATA_FOLDER / "scenario_analysis.csv",
    index=False
)

print(
    "\nScenario analysis saved successfully."
)

print("\n======================================")