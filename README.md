Supply Chain Optimization

A Python-based Supply Chain Optimization system designed to minimize overall logistics costs by optimizing inventory levels and transportation routes.

Project Overview

This project combines inventory optimization and vehicle route optimization to help businesses reduce logistics costs and improve supply chain efficiency.

The system performs:

Customer demand analysis
Warehouse capacity analysis
Vehicle capacity analysis
Distance matrix generation
Economic Order Quantity (EOQ)
Safety Stock calculation
Clarke-Wright Savings algorithm
Genetic Algorithm for route optimization
Transportation cost calculation
Inventory cost calculation
Scenario analysis
Optimized route generation
Cost analysis for Power BI visualization
Objectives
Minimize transportation costs.
Optimize inventory ordering quantities.
Calculate appropriate safety stock levels.
Optimize vehicle routes.
Analyze warehouse and vehicle capacity.
Compare different supply chain scenarios.
Calculate total logistics cost.
Provide data outputs for dashboard visualization.
Technologies Used
Python
Pandas
NumPy
Matplotlib
Git
GitHub
Power BI
Algorithms Used
1. Economic Order Quantity (EOQ)

EOQ determines the optimal quantity of inventory to order while balancing ordering and holding costs.

Formula:

EOQ = √(2DS/H)

Where:

D = Annual demand
S = Ordering cost
H = Holding cost
2. Safety Stock

Safety stock is calculated using demand variability and lead time to reduce the risk of stockouts.

3. Clarke-Wright Savings Algorithm

The Clarke-Wright algorithm combines customer routes based on distance savings to reduce transportation distance and cost.

4. Genetic Algorithm

The Genetic Algorithm searches for improved customer sequences and vehicle routes to minimize transportation cost.

Project Workflow
Input Data
    ↓
Data Analysis
    ↓
Distance Matrix
    ↓
EOQ Analysis
    ↓
Safety Stock Analysis
    ↓
Clarke-Wright Route Optimization
    ↓
Genetic Algorithm Optimization
    ↓
Transportation Cost
    ↓
Inventory Cost
    ↓
Total Logistics Cost
    ↓
Scenario Analysis
    ↓
CSV Outputs
    ↓
Power BI Dashboard
Dataset

The project uses the following data:

Customers

Contains:

Customer ID
X coordinate
Y coordinate
Demand
Vehicles

Contains:

Vehicle ID
Vehicle capacity
Cost per kilometer
Warehouse

Contains:

Warehouse ID
X coordinate
Y coordinate
Capacity
Inventory

Contains:

Product
Annual demand
Ordering cost
Holding cost
Lead time
Daily demand
Demand History

Contains historical daily demand for each product.

Current Results
Customer Analysis
Number of customers: 10
Total customer demand: 1310 units
Average customer demand: 131 units
Maximum customer demand: 200 units
Minimum customer demand: 80 units
Warehouse
Warehouse capacity: 2000 units
Capacity status: Sufficient
Vehicles
Number of vehicles: 3
Total vehicle capacity: 2000 units
EOQ
Product	EOQ
P1	866.03
P2	730.30
P3	979.80
Safety Stock
Product	Safety Stock
P1	8.01
P2	4.95
P3	9.57
Optimized Transportation

The Genetic Algorithm produced an optimized transportation cost of:

₹9,788.75

Optimized routes:

Route 1:
W1 → C2 → C6 → C7 → C9 → C10 → C8 → C5 → W1

Vehicle: V3
Demand: 940 units
Distance: 198.49 km
Cost: ₹6,947.07
Route 2:
W1 → C1 → C4 → C3 → W1

Vehicle: V1
Demand: 370 units
Distance: 113.67 km
Cost: ₹2,841.68
Inventory Cost

Total annual inventory cost:

₹52,769.86

Total Logistics Cost
Inventory Cost       ₹52,769.86
Transportation Cost  ₹ 9,788.75
--------------------------------
Total Logistics Cost ₹62,558.61
Scenario Analysis
Scenario	Inventory Cost	Transportation Cost	Total Cost
Base Scenario	₹52,769.86	₹9,788.75	₹62,558.61
Demand +10%	₹55,345.49	₹10,767.62	₹66,113.12
Transportation Cost +20%	₹52,769.86	₹11,746.50	₹64,516.36
Demand -10%	₹50,061.88	₹8,809.88	₹58,871.76
How to Run
1. Clone the repository
git clone https://github.com/saikiran-svg/Supply_Chain_Optimization.git
2. Open the project
cd Supply_Chain_Optimization
3. Create virtual environment
python -m venv .venv
4. Activate virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
6. Run the complete project
python main.py
Output Files

The project generates important analysis results inside the data/ folder:

distance_matrix.csv
optimized_routes.csv
ga_result.csv
clarke_wright_routes.csv
cost_summary.csv
scenario_analysis.csv
transportation_cost.txt

These files can be used for further analysis and Power BI dashboard development.

Power BI Dashboard

The generated CSV files can be imported into Power BI to create:

Total Logistics Cost KPI
Inventory Cost KPI
Transportation Cost KPI
Route Distance analysis
Vehicle utilization
Scenario comparison
Product-wise EOQ
Safety Stock analysis
Customer demand analysis
Optimized route analysis
Future Improvements
Real-world road distance using mapping APIs
Real-time vehicle tracking
Multiple warehouse optimization
Delivery time-window constraints
Fuel consumption optimization
Real-time demand forecasting
Interactive web dashboard
Cloud deployment
Author

Saikiran

License

This project is developed for academic and educational purposes.


### Then in VS Code

1. Open your `Supply_Chain_Optimization` folder.
2. Right-click the **root folder** → **New File**.
3. Name it exactly:
   **`README.md`**
4. Paste the entire content above.
5. Press **Ctrl + S**.
6. Open VS Code terminal and run:

```powershell
git add README.md
git commit -m "Add project README"
git push

That's it. Your GitHub repository will then show the README automatically on the repository homepage.