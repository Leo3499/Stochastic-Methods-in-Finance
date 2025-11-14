import itertools
import numpy as np
import pandas as pd

# Parameters
n = 25
S0 = 391.16
K = 391.16
r = 0.01
T = 0.5


# Load historical data
data = pd.read_csv("filtered_data.csv")
data["Close"] = data["Close.Last"].replace('[\$,]', '', regex=True).astype(float)
data["log_return"] = np.log(data["Close"] / data["Close"].shift(1))

# Compute volatility from historical returns
sigma_daily = data["log_return"].std(skipna=True)
sigma_annual = sigma_daily * np.sqrt(250)

# Time step and up/down factors
delta_t = T / n
u = np.exp(sigma_annual * np.sqrt(delta_t))
d = np.exp(-sigma_annual * np.sqrt(delta_t))

q = (np.exp(r * delta_t) - d) / (u - d)

print(f"Risk-neutral probability q = {q:.6f}")