import math
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Example usage
S = 100 # Stock price
K = 105 # Strike price
T = 0.25 # Time to expiration (in years)
r = 0.02 # Risk-free rate
sigma = 0.3 # Volatility

call_price = black_scholes(S, K, T, r, sigma, 'call')
put_price = black_scholes(S, K, T, r, sigma, 'put')

print("Call price:", call_price)
print("Put price:", put_price)
'''
This program uses the black_scholes() function to price European call and put options using the Black-Scholes option pricing model. The function takes the following parameters as inputs:

S is the current stock price
K is the strike price of the option
T is the time to expiration of the option (in years)
r is the risk-free interest rate
sigma is the volatility of the stock price
option_type is either 'call' or 'put'
The function uses the math and scipy.stats.norm libraries to calculate the option price.

Please note that, for the above code to work, you need to have the scipy library installed, you can do this by running !pip install scipy in your terminal or command prompt.

The Black-Scholes model is a widely used model for option pricing but there are other models that can be used to price options like binomial tree model, Monte Carlo simulation, etc. The choice of the model depends on the context and the level of precision you need.
'''