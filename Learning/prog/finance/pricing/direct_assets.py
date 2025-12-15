import numpy as np
import matplotlib.pyplot as plt

def simulate_asset_price(S0, r, sigma, T, steps, n_simulations):
    """
    Simulates the price of an asset under the risk-neutral measure using Geometric Brownian Motion (GBM).

    Parameters:
    S0 (float): Initial asset price
    r (float): Risk-free rate
    sigma (float): Volatility of the asset
    T (float): Time to maturity (in years)
    steps (int): Number of time steps
    n_simulations (int): Number of simulations

    Returns:
    numpy.ndarray: Simulated asset prices
    """
    dt = T / steps  # Time increment
    prices = np.zeros((n_simulations, steps + 1))  # Array to store prices
    prices[:, 0] = S0  # Initial price for all simulations

    for t in range(1, steps + 1):
        # Simulate price changes under the risk-neutral measure
        Z = np.random.standard_normal(n_simulations)  # Random draw from normal distribution
        prices[:, t] = prices[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    return prices

def visualize_simulation(S0, r, sigma, T, steps, n_simulations):
    """
    Visualizes the simulated asset prices.

    Parameters:
    S0 (float): Initial asset price
    r (float): Risk-free rate
    sigma (float): Volatility of the asset
    T (float): Time to maturity (in years)
    steps (int): Number of time steps
    n_simulations (int): Number of simulations
    """
    prices = simulate_asset_price(S0, r, sigma, T, steps, n_simulations)
    time = np.linspace(0, T, steps + 1)

    plt.figure(figsize=(10, 6))
    for i in range(n_simulations):
        plt.plot(time, prices[i, :], lw=0.8)
    plt.title('Simulated Asset Prices')
    plt.xlabel('Time (years)')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()
    plt.

# Example usage
S0 = 100  # Initial asset price
r = 0.05  # Risk-free rate
sigma = 0.2  # Volatility
T = 1  # Time to maturity in years
steps = 252  # Number of time steps (e.g., daily steps for 1 year)
n_simulations = 10  # Number of simulations

visualize_simulation(S0, r, sigma, T, steps, n_simulations)
