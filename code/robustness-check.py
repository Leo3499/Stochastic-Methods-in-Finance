

import pandas as pd
import numpy as np
import math
import os

# Parameters (constants)
n = 25
K = 391.16
T = 0.5
dt = T / n
S0 = 391.16  # Set based on your data

# Load payoffs for j = 0 to 25
payoff_data = {}
for j in range(n + 1):
    df = pd.read_csv(f"j-{j}.csv")
    payoff_data[j] = df["Payoff"].mean()

# Robustness check settings
r_values = [0.005, 0.01, 0.015, 0.02]
sigma_values = [0.15, 0.20, 0.212, 0.25, 0.30]  # 0.212 = actual volatility

def compute_q(sigma, r):
    u = math.exp(sigma * math.sqrt(dt))
    d = math.exp(-sigma * math.sqrt(dt))
    return (math.exp(r * dt) - d) / (u - d)

def backward_induction(q):
    V = np.zeros((n + 1, n + 1))
    for j in range(n + 1):
        V[n, j] = payoff_data[j]
    for t in range(n - 1, -1, -1):
        for j in range(t + 1):
            V[t, j] = math.exp(-r * dt) * (q * V[t + 1, j + 1] + (1 - q) * V[t + 1, j])
    return V[0, 0]

# Run robustness check
results = []

for r in r_values:
    sigma = 0.2  # fixed sigma
    q = compute_q(sigma, r)
    price = backward_induction(q)
    results.append({"Parameter": "r", "Value": r, "Option_Price": price})

for sigma in sigma_values:
    r = 0.01  # fixed r
    q = compute_q(sigma, r)
    price = backward_induction(q)
    results.append({"Parameter": "sigma", "Value": sigma, "Option_Price": price})

# Output results
results_df = pd.DataFrame(results)
print(results_df)