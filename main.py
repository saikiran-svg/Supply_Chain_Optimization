import subprocess
import sys

scripts = [
    "src/data_analysis.py",
    "src/distance_matrix.py",
    "src/eoq.py",
    "src/safety_stock.py",
    "src/clarke_wright.py",
    "src/genetic_algorithm.py",
    "src/cost_model.py",
    "src/scenario_analysis.py"
]

print("\n========================================")
print(" SUPPLY CHAIN OPTIMIZATION")
print("========================================\n")

for script in scripts:

    print(f"\n>>> Running {script}\n")

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:

        print(
            f"\nERROR: {script} failed."
        )

        break

else:

    print("\n========================================")
    print(" ALL ANALYSIS COMPLETED SUCCESSFULLY")
    print("========================================")