import pandas as pd
import random
from pathlib import Path

# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

# ==========================================
# LOAD DATA
# ==========================================

customers = pd.read_csv(
    DATA_FOLDER / "customers.csv"
)

vehicles = pd.read_csv(
    DATA_FOLDER / "vehicles.csv"
)

distance_matrix = pd.read_csv(
    DATA_FOLDER / "distance_matrix.csv",
    index_col=0
)

distance_matrix.index = distance_matrix.index.astype(str)
distance_matrix.columns = distance_matrix.columns.astype(str)

customers["customer_id"] = (
    customers["customer_id"].astype(str)
)

# ==========================================
# FIX RANDOM SEED
# ==========================================

random.seed(42)

# ==========================================
# CUSTOMER DATA
# ==========================================

customer_ids = customers[
    "customer_id"
].tolist()

demand = dict(
    zip(
        customers["customer_id"],
        customers["demand"].astype(float)
    )
)

# ==========================================
# VEHICLES
# ==========================================

vehicles = vehicles.sort_values(
    "capacity"
).to_dict("records")

# ==========================================
# ROUTE DISTANCE
# ==========================================

def route_distance(route):

    if not route:
        return 0.0

    distance = float(
        distance_matrix.loc[
            "W1",
            route[0]
        ]
    )

    for i in range(len(route) - 1):

        distance += float(
            distance_matrix.loc[
                route[i],
                route[i + 1]
            ]
        )

    distance += float(
        distance_matrix.loc[
            route[-1],
            "W1"
        ]
    )

    return distance


# ==========================================
# CREATE ROUTES
# ==========================================

def create_routes(customer_order):

    routes = []

    current_route = []
    current_demand = 0.0

    max_capacity = max(
        float(v["capacity"])
        for v in vehicles
    )

    for customer in customer_order:

        customer_demand = demand[customer]

        if (
            current_demand
            + customer_demand
            <= max_capacity
        ):

            current_route.append(customer)

            current_demand += customer_demand

        else:

            if current_route:
                routes.append(
                    current_route
                )

            current_route = [customer]
            current_demand = customer_demand

    if current_route:
        routes.append(current_route)

    return routes


# ==========================================
# CALCULATE TOTAL COST
# ==========================================

def calculate_cost(customer_order):

    routes = create_routes(customer_order)

    total_cost = 0.0

    for route in routes:

        route_demand = sum(
            demand[c]
            for c in route
        )

        selected_vehicle = None

        for vehicle in vehicles:

            if (
                float(vehicle["capacity"])
                >= route_demand
            ):

                selected_vehicle = vehicle
                break

        if selected_vehicle is None:
            return float("inf")

        distance = route_distance(route)

        cost = (
            distance
            * float(
                selected_vehicle[
                    "cost_per_km"
                ]
            )
        )

        total_cost += cost

    return total_cost


# ==========================================
# INITIAL POPULATION
# ==========================================

POPULATION_SIZE = 100
GENERATIONS = 200
SURVIVORS = 20

population = []

for _ in range(POPULATION_SIZE):

    solution = customer_ids.copy()

    random.shuffle(solution)

    population.append(solution)


# ==========================================
# GENETIC ALGORITHM
# ==========================================

for generation in range(GENERATIONS):

    scored_population = []

    for solution in population:

        cost = calculate_cost(solution)

        scored_population.append(
            (cost, solution)
        )

    scored_population.sort(
        key=lambda x: x[0]
    )

    survivors = [
        solution.copy()
        for cost, solution
        in scored_population[:SURVIVORS]
    ]

    new_population = survivors.copy()

    while len(new_population) < POPULATION_SIZE:

        parent = random.choice(
            survivors
        )

        child = parent.copy()

        i, j = random.sample(
            range(len(child)),
            2
        )

        child[i], child[j] = (
            child[j],
            child[i]
        )

        new_population.append(child)

    population = new_population


# ==========================================
# FIND FINAL BEST SOLUTION
# ==========================================

best_solution = min(
    population,
    key=calculate_cost
)

best_cost = calculate_cost(
    best_solution
)

best_routes = create_routes(
    best_solution
)


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\n========== GENETIC ALGORITHM ==========")

print(
    f"Best transportation cost: "
    f"₹{best_cost:.2f}"
)

print("\nBest customer sequence:")

print(
    " → ".join(best_solution)
)

print("\nOptimized Routes:")

route_results = []

for route_number, route in enumerate(
    best_routes,
    start=1
):

    route_demand = sum(
        demand[c]
        for c in route
    )

    selected_vehicle = None

    for vehicle in vehicles:

        if (
            float(vehicle["capacity"])
            >= route_demand
        ):

            selected_vehicle = vehicle
            break

    if selected_vehicle is None:

        print(
            f"Route {route_number}: "
            "NO SUITABLE VEHICLE"
        )

        continue

    distance = route_distance(route)

    vehicle_id = selected_vehicle[
        "vehicle_id"
    ]

    vehicle_capacity = selected_vehicle[
        "capacity"
    ]

    cost_per_km = float(
        selected_vehicle[
            "cost_per_km"
        ]
    )

    route_cost = (
        distance
        * cost_per_km
    )

    print(
        f"\nRoute {route_number}: "
        f"W1 → "
        f"{' → '.join(route)}"
        f" → W1"
    )

    print(
        f"Vehicle: {vehicle_id}"
    )

    print(
        f"Vehicle capacity: "
        f"{vehicle_capacity} units"
    )

    print(
        f"Demand: "
        f"{route_demand:.0f} units"
    )

    print(
        f"Distance: "
        f"{distance:.2f} km"
    )

    print(
        f"Cost: "
        f"₹{route_cost:.2f}"
    )

    route_results.append({
        "route": route_number,
        "vehicle": vehicle_id,
        "demand": round(route_demand, 2),
        "distance_km": round(distance, 2),
        "transportation_cost": round(
            route_cost,
            2
        )
    })


# ==========================================
# SAVE FINAL GA COST
# ==========================================

ga_result = pd.DataFrame({
    "transportation_cost": [
        round(best_cost, 2)
    ]
})

ga_result.to_csv(
    DATA_FOLDER / "ga_result.csv",
    index=False
)


# ==========================================
# SAVE OPTIMIZED ROUTES
# ==========================================

routes_df = pd.DataFrame(
    route_results
)

routes_df.to_csv(
    DATA_FOLDER / "optimized_routes.csv",
    index=False
)

print(
    "\nTransportation cost saved successfully."
)

print(
    f"Saved GA cost: "
    f"₹{best_cost:.2f}"
)

print("\n=======================================")