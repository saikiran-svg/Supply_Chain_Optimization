import pandas as pd
from pathlib import Path

# Get the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data folder
DATA_FOLDER = PROJECT_ROOT / "data"

# File paths
customers_file = DATA_FOLDER / "customers.csv"
warehouse_file = DATA_FOLDER / "warehouse.csv"
vehicles_file = DATA_FOLDER / "vehicles.csv"
inventory_file = DATA_FOLDER / "inventory.csv"


# -----------------------------
# CHECK FILES
# -----------------------------

files = {
    "customers.csv": customers_file,
    "warehouse.csv": warehouse_file,
    "vehicles.csv": vehicles_file,
    "inventory.csv": inventory_file
}

for file_name, file_path in files.items():

    if not file_path.exists():
        print(f"ERROR: {file_name} not found.")
        print(f"Expected location: {file_path}")
        exit()

    if file_path.stat().st_size == 0:
        print(f"ERROR: {file_name} is empty.")
        print(f"Please add data to: {file_path}")
        exit()


# -----------------------------
# LOAD DATA
# -----------------------------

customers = pd.read_csv(customers_file)
warehouse = pd.read_csv(warehouse_file)
vehicles = pd.read_csv(vehicles_file)
inventory = pd.read_csv(inventory_file)


# -----------------------------
# CUSTOMER ANALYSIS
# -----------------------------

print("\n========== CUSTOMER ANALYSIS ==========")

print("Number of customers:", len(customers))

print(
    "Total customer demand:",
    customers["demand"].sum(),
    "units"
)

print(
    "Average customer demand:",
    round(customers["demand"].mean(), 2),
    "units"
)

print(
    "Maximum customer demand:",
    customers["demand"].max(),
    "units"
)

print(
    "Minimum customer demand:",
    customers["demand"].min(),
    "units"
)


# -----------------------------
# WAREHOUSE ANALYSIS
# -----------------------------

print("\n========== WAREHOUSE ==========")

print(
    "Warehouse capacity:",
    warehouse["capacity"].sum(),
    "units"
)


# -----------------------------
# VEHICLE ANALYSIS
# -----------------------------

print("\n========== VEHICLES ==========")

print("Number of vehicles:", len(vehicles))

print(
    "Total vehicle capacity:",
    vehicles["capacity"].sum(),
    "units"
)

print("\nVehicle details:")
print(vehicles.to_string(index=False))


# -----------------------------
# INVENTORY ANALYSIS
# -----------------------------

print("\n========== INVENTORY ==========")

print(
    "Number of products:",
    len(inventory)
)

print(
    "Total annual demand:",
    inventory["annual_demand"].sum(),
    "units"
)

print("\nInventory details:")
print(inventory.to_string(index=False))


# -----------------------------
# CAPACITY CHECK
# -----------------------------

total_demand = customers["demand"].sum()
warehouse_capacity = warehouse["capacity"].sum()
vehicle_capacity = vehicles["capacity"].sum()

print("\n========== CAPACITY CHECK ==========")

if total_demand <= warehouse_capacity:
    print("Warehouse capacity: SUFFICIENT")
else:
    print("Warehouse capacity: NOT SUFFICIENT")

if total_demand <= vehicle_capacity:
    print("Vehicle capacity: SUFFICIENT")
else:
    print("Vehicle capacity: NOT SUFFICIENT")


print("\n====================================")
print("DATA ANALYSIS COMPLETED SUCCESSFULLY")
print("====================================")