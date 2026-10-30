# Inventory-Optimization-Model
Stochastic Inventory Optimization Model Using Monte Carlo Simulation
# 📦 Stochastic Inventory Optimization Model Using Monte Carlo Simulation

### Optimizing Retail Inventory Levels Under Uncertain Customer Demand

## 📌 Project Overview

The **Stochastic Inventory Optimization Model** is a Python-based project that determines the optimal inventory quantity a retailer should order when future customer demand is uncertain.

Retail businesses often face difficulties deciding how much stock to maintain. Ordering too much can result in unsold inventory and financial losses, while ordering too little can lead to lost sales and reduced customer satisfaction.

This project uses **Monte Carlo Simulation and Stochastic Optimization** to evaluate different inventory quantities under uncertain demand and identify the quantity that maximizes expected profit.

## 🎯 Objectives

- Develop a stochastic optimization model for inventory management.
- Represent uncertain customer demand using probability distributions.
- Apply Monte Carlo Simulation to generate different demand scenarios.
- Determine the optimal inventory ordering quantity.
- Maximize expected profit while minimizing inventory-related losses.
- Perform sensitivity analysis by changing demand probabilities and cost parameters.
- Compare stochastic optimization results with a deterministic baseline.

## 🏪 Real-World Problem

Consider a retail store that must decide how many products to purchase before knowing actual customer demand.

The store faces two possible demand scenarios:

| Demand Scenario | Probability | Average Demand |
|---|---:|---:|
| Normal Demand | 80% | 80 units |
| High Demand | 20% | 150 units |

Actual demand is uncertain and follows a Poisson distribution within each scenario.

The model evaluates different ordering quantities and identifies the quantity that provides the highest expected profit.

## 📐 Mathematical Formulation

### Decision Variable

- `Q` = Number of units ordered by the retailer.

### Uncertain Parameter

- `D` = Actual customer demand.

### Financial Parameters

| Parameter | Value |
|---|---:|
| Selling Price | ₹100 |
| Purchase Cost | ₹60 |
| Unsold Inventory Recovery Value | ₹20 |
| Normal Demand Probability | 0.80 |
| High Demand Probability | 0.20 |

### Profit Function

The profit for a given ordering quantity and actual demand is:

Profit = (Selling Price × Units Sold) + (Recovery Value × Unsold Units) − (Purchase Cost × Ordered Units)

Mathematically:

Profit(Q,D) = 100 × min(Q,D) + 20 × max(Q−D,0) − 60 × Q

### Optimization Objective

Maximize expected profit:

Maximize E[Profit(Q,D)]

Subject to:

- Q ≥ 0
- Q must be an integer.
- Inventory ordering quantity cannot be negative.

## 🧠 Methodology

The project follows these steps:

1. **Problem Identification:** Identify inventory management under uncertain customer demand.
2. **Probability Distribution:** Model demand using a mixture of two Poisson distributions.
3. **Monte Carlo Simulation:** Generate multiple random demand scenarios.
4. **Stochastic Optimization:** Evaluate expected profit for different ordering quantities.
5. **Optimal Solution:** Select the ordering quantity that maximizes expected profit.
6. **Sensitivity Analysis:** Examine the effect of changes in demand probabilities and financial parameters.
7. **Deterministic Comparison:** Compare the stochastic solution with an approach based on expected demand.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NumPy | Numerical computation and random simulations |
| Pandas | Dataset management and analysis |
| Matplotlib | Data visualization |
| VS Code | Development environment |
| Monte Carlo Simulation | Modeling uncertain demand |

## 📂 Project Structure

```text
Stochastic-Inventory-Optimization/
│
├── data/
│   └── inventory_data.csv
│
├── results/
│   ├── optimization_results.csv
│   └── sensitivity_analysis.csv
│
├── src/
│   └── inventory_optimization.py
│
├── notebooks/
│   └── inventory_analysis.ipynb
│
├── README.md
├── requirements.txt
└── .gitignore
```

*The files and folders will be created as we implement the project.*

## ⚙️ Installation and Execution

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the Project Directory

```bash
cd Stochastic-Inventory-Optimization
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Project

```bash
python src/inventory_optimization.py
```

## 📊 Expected Results

The project will generate:

- Optimal inventory ordering quantity.
- Expected profit under uncertain demand.
- Average simulated demand.
- Profit variability across simulation runs.
- Comparison between stochastic and deterministic decisions.
- Sensitivity analysis results.
- Graphs showing the relationship between inventory quantity and expected profit.

*Actual numerical results will be added after implementing and executing the optimization model.*

## 📈 Sensitivity Analysis

The model will examine how changes in the following parameters affect the optimal inventory decision:

- Normal demand probability.
- High demand probability.
- Selling price.
- Purchase cost.
- Unsold inventory recovery value.
- Average customer demand.

## 🔍 Stochastic vs Deterministic Optimization

The project compares two approaches:

**Stochastic Optimization**
- Considers multiple possible demand outcomes.
- Uses probability distributions.
- Maximizes expected profit across simulated scenarios.

**Deterministic Optimization**
- Uses average expected demand as a fixed value.
- Does not explicitly account for demand variability.

The comparison demonstrates the importance of considering uncertainty in real-world inventory decisions.

## 🌍 Real-World Applications

This optimization model can be applied to:

- Supermarkets and retail stores.
- E-commerce inventory management.
- Warehouse stock planning.
- Pharmaceutical inventory management.
- Supply chain management.
- Manufacturing and production planning.

## 🎓 Academic Information

**Course:** 21AIE321T – Stochastic Decision Making

**Assignment:** Assignment IV – Mini Project: Stochastic Optimization Model

**Institution:** SRM Institute of Science and Technology, Tiruchirappalli

**Academic Year:** 2026–2027

## 👨‍💻 Project Status

🚧 In Development

The project will be developed incrementally, beginning with mathematical formulation, followed by Python implementation, optimization, simulation, sensitivity analysis and documentation.

## 📜 License

This project is developed for academic and educational purposes.
