import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure output directories exist
os.makedirs("results", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ---------------------------------------------------------
# 1. Model Parameters
# ---------------------------------------------------------
SELLING_PRICE = 100.0
PURCHASE_COST = 60.0
SALVAGE_VALUE = 20.0

P_NORMAL = 0.80
P_HIGH = 0.20
LAMBDA_NORMAL = 80
LAMBDA_HIGH = 150

N_SIMULATIONS = 50_000
SEED = 42

np.random.seed(SEED)

print("=" * 60)
print("STOCHASTIC INVENTORY OPTIMIZATION MODEL")
print("=" * 60)

# ---------------------------------------------------------
# 2. Demand Simulation (Mixture of Poisson Distributions)
# ---------------------------------------------------------
def generate_demand(n_sims=N_SIMULATIONS, p_high=P_HIGH, lam_norm=LAMBDA_NORMAL, lam_high=LAMBDA_HIGH):
    # Vectorized scenario selection: 1 = High, 0 = Normal
    scenarios = np.random.binomial(n=1, p=p_high, size=n_sims)
    
    demand_normal = np.random.poisson(lam=lam_norm, size=n_sims)
    demand_high = np.random.poisson(lam=lam_high, size=n_sims)
    
    # Combined mixture demand
    demand = np.where(scenarios == 1, demand_high, demand_normal)
    return demand, scenarios

demand_simulated, scenarios_simulated = generate_demand()

# Save sample simulation data
df_data = pd.DataFrame({
    "Scenario": np.where(scenarios_simulated == 1, "High", "Normal"),
    "Simulated_Demand": demand_simulated
})
df_data.head(5000).to_csv("data/inventory_data.csv", index=False)
print(f"Generated {N_SIMULATIONS:,} demand scenarios.")
print(f"Simulated Mean Demand: {demand_simulated.mean():.2f} units (Theoretical E[D] = 94.00 units)\n")

# ---------------------------------------------------------
# 3. Vectorized Profit Evaluation
# ---------------------------------------------------------
def evaluate_profit(Q, demand, price=SELLING_PRICE, cost=PURCHASE_COST, salvage=SALVAGE_VALUE):
    sold = np.minimum(Q, demand)
    unsold = np.maximum(Q - demand, 0)
    profit = (price * sold) + (salvage * unsold) - (cost * Q)
    return profit

Q_candidates = np.arange(40, 181, 1)
expected_profits = []
std_profits = []

for q in Q_candidates:
    profits_q = evaluate_profit(q, demand_simulated)
    expected_profits.append(np.mean(profits_q))
    std_profits.append(np.std(profits_q))

results_df = pd.DataFrame({
    "Order_Quantity_Q": Q_candidates,
    "Expected_Profit": expected_profits,
    "Std_Profit": std_profits
})
results_df.to_csv("results/optimization_results.csv", index=False)

# Optimal Quantity
best_idx = np.argmax(expected_profits)
Q_optimal = int(Q_candidates[best_idx])
max_expected_profit = expected_profits[best_idx]

# ---------------------------------------------------------
# 4. Stochastic vs. Deterministic Comparison
# ---------------------------------------------------------
Q_deterministic = int(round(P_NORMAL * LAMBDA_NORMAL + P_HIGH * LAMBDA_HIGH)) # 94 units
profit_stochastic = evaluate_profit(Q_optimal, demand_simulated)
profit_deterministic = evaluate_profit(Q_deterministic, demand_simulated)

mean_stoch_profit = np.mean(profit_stochastic)
mean_det_profit = np.mean(profit_deterministic)
vss = mean_stoch_profit - mean_det_profit  # Value of Stochastic Solution

print(f"--- OPTIMIZATION FINDINGS ---")
print(f"Optimal Stochastic Order Quantity (Q*): {Q_optimal} units")
print(f"Max Expected Profit: Rs. {max_expected_profit:,.2f}")
print(f"Deterministic Order Quantity (Q_det): {Q_deterministic} units")
print(f"Deterministic Expected Profit: Rs. {mean_det_profit:,.2f}")
print(f"Value of Stochastic Solution (VSS): Rs. {vss:,.2f} increase per cycle\n")

# ---------------------------------------------------------
# 5. Sensitivity Analysis
# ---------------------------------------------------------
print("Running Sensitivity Analysis...")
sensitivity_records = []

# Vary High Demand Probability from 0.05 to 0.45
for p_h in np.linspace(0.05, 0.45, 9):
    dem, _ = generate_demand(p_high=p_h)
    best_q = max(Q_candidates, key=lambda q: np.mean(evaluate_profit(q, dem)))
    exp_prof = np.mean(evaluate_profit(best_q, dem))
    sensitivity_records.append({
        "Parameter": "P(High Demand)",
        "Parameter_Value": round(p_h, 2),
        "Optimal_Q": best_q,
        "Expected_Profit": round(exp_prof, 2)
    })

# Vary Purchase Cost from Rs. 40 to Rs. 80
for c in [40, 50, 60, 70, 80]:
    best_q = max(Q_candidates, key=lambda q: np.mean(evaluate_profit(q, demand_simulated, cost=c)))
    exp_prof = np.mean(evaluate_profit(best_q, demand_simulated, cost=c))
    sensitivity_records.append({
        "Parameter": "Purchase Cost",
        "Parameter_Value": c,
        "Optimal_Q": best_q,
        "Expected_Profit": round(exp_prof, 2)
    })

sens_df = pd.DataFrame(sensitivity_records)
sens_df.to_csv("results/sensitivity_analysis.csv", index=False)
print("Saved sensitivity analysis to results/sensitivity_analysis.csv\n")

# ---------------------------------------------------------
# 6. Generate Presentation-Quality Visualizations
# ---------------------------------------------------------
plt.style.use('ggplot')

# Chart 1: Demand Distribution
plt.figure(figsize=(9, 5))
plt.hist(demand_simulated, bins=60, color='#3498db', edgecolor='black', alpha=0.75, density=True)
plt.axvline(np.mean(demand_simulated), color='red', linestyle='--', linewidth=2, label=f'Mean Demand ({np.mean(demand_simulated):.1f})')
plt.title("Simulated Customer Demand (Bimodal Poisson Mixture)")
plt.xlabel("Demand (Units)")
plt.ylabel("Probability Density")
plt.legend()
plt.tight_layout()
plt.savefig("results/demand_distribution.png", dpi=300)
plt.close()

# Chart 2: Expected Profit vs Order Quantity (Q)
plt.figure(figsize=(9, 5))
plt.plot(Q_candidates, expected_profits, color='#2c3e50', linewidth=2.5, label='E[Profit]')
plt.axvline(Q_optimal, color='#27ae60', linestyle='--', linewidth=2, label=f'Stochastic Optimal Q* = {Q_optimal}')
plt.axvline(Q_deterministic, color='#e74c3c', linestyle=':', linewidth=2, label=f'Deterministic Q = {Q_deterministic}')
plt.scatter([Q_optimal], [max_expected_profit], color='#27ae60', s=100, zorder=5)
plt.title("Expected Profit vs. Inventory Order Quantity (Q)")
plt.xlabel("Order Quantity (Q)")
plt.ylabel("Expected Profit (Rs.)")
plt.legend()
plt.tight_layout()
plt.savefig("results/expected_profit_vs_Q.png", dpi=300)
plt.close()

# Chart 3: Stochastic vs Deterministic Profit Distribution
plt.figure(figsize=(9, 5))
plt.boxplot([profit_stochastic, profit_deterministic], patch_artist=True,
            boxprops=dict(facecolor='#aed6f1', color='#1b4f72'),
            medianprops=dict(color='#b03a2e', linewidth=2))
plt.xticks([1, 2], [f"Stochastic (Q={Q_optimal})", f"Deterministic (Q={Q_deterministic})"])
plt.title("Profit Distribution Comparison: Stochastic vs. Deterministic")
plt.ylabel("Realized Profit (Rs.)")
plt.tight_layout()
plt.savefig("results/stochastic_vs_deterministic_profit.png", dpi=300)
plt.close()

print("All charts generated and saved in results/ directory.")
print("=" * 60)
print("PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
print("=" * 60)