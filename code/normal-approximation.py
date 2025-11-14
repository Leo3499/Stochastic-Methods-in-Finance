

import pandas as pd
import numpy as np
from scipy.stats import norm
import os

# Set working directory
os.chdir("/Users/leonardogonnelli/Desktop/Stochastic Methods/Assignment")

# Parameters
K = 391.16
r = 0.01
T = 0.5

# Load all CSVs and combine into a single DataFrame
dfs = []
for j in range(26):
    df_j = pd.read_csv(f"j-{j}.csv")
    dfs.append(df_j)
df_all = pd.concat(dfs, ignore_index=True)

# Compute empirical mean and std deviation of the average prices
mu = df_all["Average_Price"].mean()
sigma = df_all["Average_Price"].std()

# Normal approximation for Asian call option
d = (mu - K) / sigma
expected_payoff = (mu - K) * norm.cdf(d) + sigma * norm.pdf(d)
discounted_price = np.exp(-r * T) * expected_payoff

# Output result
print(f"Normal approximation price for the Asian call option: {discounted_price:.4f}")