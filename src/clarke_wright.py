import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

customers = pd.read_csv(DATA_FOLDER / "customers.csv")
vehicles = pd.read_csv(DATA_FOLDER / "vehicles.csv")

distance_matrix = pd.read_csv(
    DATA_FOLDER / "distance_matrix.csv",
    index_col=0
)

distance_matrix.index = distance_matrix.index.astype(str)
distance_matrix.columns = distance_matrix.columns.astype(str)

customers["customer_id"] = customers["customer_id"].astype(str)

# -------------------------------------------------
# CALCULATE SAVINGS
# -------------------------------------------------

savings = []

for i in range(len(customers)):
    for j in range(i + 1, len(customers)):

        ci = customers.iloc[i]["customer_id"]
        cj = customers.iloc[j]["customer_id"]

        saving = (
            float(distance_matrix.loc["W1", ci])
            + float(distance_matrix.loc["W1", cj])
            - float(distance_matrix.loc[ci, cj])
        )

        savings.append({
            "customer_i": ci,
            "customer_j": cj,
            "saving": saving
        })

savings_df = pd.DataFrame(savings)

savings_df = savings_df.sort_values(
    "saving",
    ascending=False
).reset_index(drop=True)

print("\n========== SAVINGS ==========")
print(savings_df.round(2).to_string(index=False))

# -------------------------------------------------
# INITIAL ROUTES
# -------------------------------------------------

routes = {}

for _, row in customers.iterrows():

    cid = row["customer_id"]

    routes[cid] = {
        "customers": [cid],
        "demand": float(row["demand"])
    }


def find_route(customer):

    for route_id, route in routes.items():

        if customer in route["customers"]:
            return route_id

    return None


# -------------------------------------------------
# MERGE ROUTES
# -------------------------------------------------

max_capacity = float(vehicles["capacity"].max())

for _, row in savings_df.iterrows():

    ci = row["customer_i"]
    cj = row["customer_j"]

    ri = find_route(ci)
    rj = find_route(cj)

    if ri is None or rj is None:
        continue

    if ri == rj:
        continue

    route_i = routes[ri]
    route_j = routes[rj]

    combined_demand = (
        route_i["demand"]
        + route_j["demand"]
    )

    if combined_demand <= max_capacity:

        routes[ri] = {
            "customers":
                route_i["customers"]
                + route_j["customers"],

            "demand":
                combined_demand
        }

        del routes[rj]


# -------------------------------------------------
# ROUTE DISTANCE
# -------------------------------------------------

def calculate_route_distance(customer_list):

    if not customer_list:
        return 0.0

    distance = float(
        distance_matrix.loc[
            "W1",
            customer_list[0]
        ]
    )

    for i in range(len(customer_list) - 1):

        distance += float(
            distance_matrix.loc[
                customer_list[i],
                customer_list[i + 1]
            ]
        )

    distance += float(
        distance_matrix.loc[
            customer_list[-1],
            "W1"
        ]
    )

    return round(distance, 2)


# -------------------------------------------------
# VEHICLE ASSIGNMENT
# -------------------------------------------------

vehicles_sorted = vehicles.sort_values(
    "capacity"
).to_dict("records")

print("\n========== CLARKE-WRIGHT ROUTES ==========")

total_distance = 0.0
total_cost = 0.0

route_results = []

for route_number, route in enumerate(
    routes.values(),
    start=1
):

    demand = route["demand"]

    selected_vehicle = None

    for vehicle in vehicles_sorted:

        if float(vehicle["capacity"]) >= demand:
            selected_vehicle = vehicle
            break

    if selected_vehicle is None:

        print(
            f"\nRoute {route_number}: "
            "NO SUITABLE VEHICLE"
        )

        continue

    route_distance = calculate_route_distance(
        route["customers"]
    )

    route_cost = (
        route_distance
        * float(selected_vehicle["cost_per_km"])
    )

    total_distance += route_distance
    total_cost += route_cost

    vehicle_id = selected_vehicle["vehicle_id"]

    print(
        f"\nRoute {route_number}: "
        f"W1 → "
        f"{' → '.join(route['customers'])}"
        f" → W1"
    )

    print(f"Vehicle: {vehicle_id}")
    print(
        f"Vehicle capacity: "
        f"{selected_vehicle['capacity']} units"
    )
    print(f"Demand: {demand:.0f} units")
    print(f"Distance: {route_distance:.2f} km")
    print(f"Cost: ₹{route_cost:.2f}")

    route_results.append({
        "route": route_number,
        "vehicle": vehicle_id,
        "demand": round(demand, 2),
        "distance_km": route_distance,
        "transportation_cost": round(route_cost, 2)
    })


# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

print("\n========== TRANSPORTATION SUMMARY ==========")

print(f"Total distance: {total_distance:.2f} km")
print(f"Total transportation cost: ₹{total_cost:.2f}")

print("\n============================================")

# Save Clarke-Wright results
pd.DataFrame(route_results).to_csv(
    DATA_FOLDER / "clarke_wright_routes.csv",
    index=False
)