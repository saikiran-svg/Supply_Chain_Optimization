import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

customers = pd.read_csv(
    DATA_FOLDER / "customers.csv"
)

warehouse = pd.read_csv(
    DATA_FOLDER / "warehouse.csv"
)

locations = pd.concat([
    warehouse[
        ["warehouse_id", "x", "y"]
    ].rename(
        columns={
            "warehouse_id": "location_id"
        }
    ),

    customers[
        ["customer_id", "x", "y"]
    ].rename(
        columns={
            "customer_id": "location_id"
        }
    )
], ignore_index=True)


def calculate_distance(
    x1, y1, x2, y2
):

    return np.sqrt(
        (x2 - x1) ** 2
        + (y2 - y1) ** 2
    )


distance_matrix = pd.DataFrame(
    index=locations["location_id"],
    columns=locations["location_id"],
    dtype=float
)

for i in range(len(locations)):

    for j in range(len(locations)):

        x1 = locations.iloc[i]["x"]
        y1 = locations.iloc[i]["y"]

        x2 = locations.iloc[j]["x"]
        y2 = locations.iloc[j]["y"]

        distance_matrix.iloc[i, j] = (
            calculate_distance(
                x1, y1, x2, y2
            )
        )


print("\n========== DISTANCE MATRIX ==========")

print(
    distance_matrix
    .round(2)
    .to_string()
)

distance_matrix.to_csv(
    DATA_FOLDER / "distance_matrix.csv"
)

print(
    "\nDistance matrix saved successfully."
)