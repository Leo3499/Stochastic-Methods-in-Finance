import numpy as np
import pandas as pd
import os

K = 391.16  # Strike price 
# Parameters
n = 25
r = 0.01
T = 0.5
delta_t = T / n
discount = np.exp(-r * delta_t)

# Risk-neutral probability (from earlier computation)
q = 0.496465

# Load all payoffs from CSVs into a single list (indexed by up-move count)
payoff_by_upmoves = []

for j in range(n + 1):
    filename = f"j-{j}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        avg_payoff = df["Payoff"].mean()
        payoff_by_upmoves.append(avg_payoff)
    else:
        payoff_by_upmoves.append(0.0)

# Backward induction
V = np.zeros((n + 1, n + 1))  # V[t][j] = option value at time t with j up-moves
V[n, :] = payoff_by_upmoves  # Fill final payoffs

for t in range(n - 1, -1, -1):
    for j in range(t + 1):
        V[t, j] = discount * (q * V[t + 1, j + 1] + (1 - q) * V[t + 1, j])

# Final result: option price at t = 0
asian_option_price = V[0, 0]
print(f"Asian Option Price at t=0: {asian_option_price:.4f}")
