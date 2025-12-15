import numpy as np
from scipy.stats import norm
import numpy as np
import pandas as pd

def simulate_asset_price(S0, r, sigma, T, steps, n_simulations):
    """
    Simulates the price of an asset under the risk-neutral measure using Geometric Brownian Motion (GBM).

    Parameters:
    S0 (float): Initial asset price
    r (float): Risk-free rate-
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


def price_european_call(S0, K, r, sigma, T, steps, n_simulations):
    """
    Prices a European call option using Monte Carlo simulation under the risk-neutral measure.

    Parameters:
    S0 (float): Initial asset price
    K (float): Strike price
    r (float): Risk-free rate
    sigma (float): Volatility of the asset
    T (float): Time to maturity (in years)
    steps (int): Number of time steps
    n_simulations (int): Number of simulations

    Returns:
    float: Price of the European call option
    """
    prices = simulate_asset_price(S0, r, sigma, T, steps, n_simulations)
    payoff = np.maximum(prices[:, -1] - K, 0)  # Payoff of the call option at maturity
    option_price = np.exp(-r * T) * np.mean(payoff)  # Discounted expected payoff.py
    return option_price


def simulate_asset_price_real_world(S0, mu, sigma, T, steps, n_simulations):
    """
    Simulate asset price under the real-world probability measure.

    Parameters:
    S0 (float): Initial asset price
    mu (float): Real-world drift (expected return)
    sigma (float): Volatility of the asset
    T (float): Time to maturity (in years)
    steps (int): Number of time steps
    n_simulations (int): Number of simulations

    Returns:
    numpy.ndarray: Simulated asset prices under the real-world measure
    """
    dt = T / steps
    prices = np.zeros((n_simulations, steps + 1))
    prices[:, 0] = S0

    for t in range(1, steps + 1):
        Z = np.random.standard_normal(n_simulations)
        prices[:, t] = prices[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    return prices

def vasicek_irb(r, a, b, sigma, t, n=12):
    """
    Function to simulate default probabilities using the Vasicek IRB model
    """
    dt = t/n
    r = np.zeros(n+1)
    r[0] = r
    for i in range(1, n+1):
        r[i] = r[i-1] + a*(b-r[i-1])*dt + sigma*np.sqrt(dt)*np.random.normal()
    return r

if __name__ == "__main__":
    # Example usage
    S0 = 100  # Initial price
    r = 0.05  # Risk-free rate
    sigma = 0.2  # Volatility (20%)
    T = 1  # 1 year to maturity
    steps = 100  # Number of time steps
    n_simulations = 1000  # Number of simulations

    prices = simulate_asset_price(S0, r, sigma, T, steps, n_simulations)
    print(prices[-1])  # Final simulated prices at maturity

    # Real-world vs Risk-neutral comparison
    mu = 0.08  # Real-world expected return (drift)
    real_world_prices = simulate_asset_price_real_world(S0, mu, sigma, T, steps, n_simulations)

    # Compute and compare expected returns under both measures
    expected_real_world_return = np.mean(real_world_prices[:, -1]) / S0 - 1
    expected_risk_neutral_return = np.mean(prices[:, -1]) / S0 - 1

    print(f"Expected real-world return: {expected_real_world_return * 100:.2f}%")
    print(f"Expected risk-neutral return: {expected_risk_neutral_return * 100:.2f}%")

    # Example usage
    K = 105  # Strike price
    call_price = price_european_call(S0, K, r, sigma, T, steps, n_simulations)
    print(f"European call option price: {call_price}")


