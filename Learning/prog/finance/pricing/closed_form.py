def black_scholes_call(S, K, r, T, sigma):
    """
    Black-Scholes formula for European call option pricing.

    Parameters:
    S (float): Current stock price
    K (float): Strike price
    r (float): Risk-free rate
    T (float): Time to maturity (in years)
    sigma (float): Volatility

    Returns:
    float: Price of the European call option
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price


if __name__ == "__main__":
    # Example usage
    S0 = 100  # Initial price
    r = 0.05  # Risk-free rate
    sigma = 0.2  # Volatility (20%)
    T = 1  # 1 year to maturity
    # Example usage
    K = 105  # Strike price

    # Example usage
    bs_call_price = black_scholes_call(S0, K, r, T, sigma)
    print(f"Black-Scholes call option price: {bs_call_price}")
