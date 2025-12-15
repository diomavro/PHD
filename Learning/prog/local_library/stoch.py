import numpy as np
from enum import Enum, auto

class StochasticProcessType(Enum):
    BROWNIAN_MOTION = auto()
    GEOMETRIC_BROWNIAN = auto()
    MEAN_REVERTING = auto()

class StochasticProcessGenerator:
    def __init__(self, process_type: StochasticProcessType, num_steps: int, dt: float, mu: float=0, sigma: float=1, mean_reversion_speed: float=0.1, mean_reversion_level: float=0):
        self.process_type = process_type
        self.num_steps = num_steps
        self.dt = dt
        self.mu = mu
        self.sigma = sigma
        self.mean_reversion_speed = mean_reversion_speed
        self.mean_reversion_level = mean_reversion_level

    def generate_process(self):
        if self.process_type == StochasticProcessType.BROWNIAN_MOTION:
            return self._generate_brownian_motion()
        elif self.process_type == StochasticProcessType.GEOMETRIC_BROWNIAN:
            return self._generate_geometric_brownian_motion()
        elif self.process_type == StochasticProcessType.MEAN_REVERTING:
            return self._generate_mean_reverting_process()

    def _generate_brownian_motion(self):
        return np.cumsum(np.random.normal(self.mu * self.dt, self.sigma * np.sqrt(self.dt), self.num_steps))

    def _generate_geometric_brownian_motion(self):
        steps = np.random.normal(self.mu * self.dt, self.sigma * np.sqrt(self.dt), self.num_steps)
        return np.cumprod(1 + steps)

    def _generate_mean_reverting_process(self):
        prices = [self.mean_reversion_level]
        for _ in range(self.num_steps - 1):
            noise = np.random.normal(0, self.sigma * np.sqrt(self.dt))
            change = self.mean_reversion_speed * (self.mean_reversion_level - prices[-1]) * self.dt + noise
            prices.append(prices[-1] + change)
        return np.array(prices)

