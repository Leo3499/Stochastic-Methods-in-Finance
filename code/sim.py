import itertools
import numpy as np
import pandas as pd

# Parameters
n = 25  # Reduced for demonstration purposes
S0 = 391.16
u = 1.05
d = 0.95
K = 391.16
r = 0.01
T = 0.5

for j in range(n + 1):
    up_combinations = list(itertools.combinations(range(1, n+1), j))

    average_prices = []
    payoffs = []

    for up_pos in up_combinations:
        path = [S0]
        for t in range(1, n+1):
            prev_price = path[-1]
            if t in up_pos:
                path.append(prev_price * u)
            else:
                path.append(prev_price * d)
        avg_price = np.mean(path)
        payoff = max(avg_price - K, 0)
        average_prices.append(avg_price)
        payoffs.append(payoff)

    df = pd.DataFrame({
        "Up_Moves": [j]*len(average_prices),
        "Average_Price": average_prices,
        "Payoff": payoffs
    })

    df.to_csv(f"j-{j}.csv", index=False)