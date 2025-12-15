
import numpy as np
from typing import List, Tuple

def payoff_call(strike_price: float, spot_price: float) -> float:
    """Calculate the payoff for a call option given the strike price and spot price"""
    return max(0.0, spot_price - strike_price)

def payoff_put(strike_price: float, spot_price: float) -> float:
    """Calculate the payoff for a put option given the strike price and spot price"""
    return max(0.0, strike_price - spot_price)

def price_put(strike: float, prices: List[float]) -> float:
    """
    Calculates the price of a put option.

    Args:
        strike (float): The strike price of the put option.
        prices (list): A list of spot prices for the underlying asset.

    Returns:
        float: The price of the put option.
    """
    res = sum([payoff_put(strike, s) for s in prices])
    return res/len(prices)

def price_call(strike: float, prices: List[float]) -> float:
    """
    Calculates the price of a call option.

    Args:
        strike (float): The strike price of the call option.
        prices (list): A list of spot prices for the underlying asset.

    Returns:
        float: The price of the call option.
    """
    res = sum([payoff_call(strike, s) for s in prices])
    return res/len(prices)