import numpy as np

from casetta.modules.base_module import BaseModule
from casetta.utils.types import GridOutput
import gymnasium as gym

class Grid(BaseModule):
    def __init__(self, config):
        super().__init__(config)
        self.energy_prices = {
            'buy': config['grid']['buy_energy'],  # $ per kWh
            'sell': config['grid']['sell_energy'],   # $ per kWh
        }
        self.action_space = gym.spaces.Box(
            low=np.array([]),
            high=np.array([]),
        )
        self.action_names = []
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([100.0, 100.0, 100.0, 100.0]),
        )

    def step(self, state, action) -> GridOutput:
        return GridOutput(
            buy_price=self.energy_prices['buy'],
            sell_price=self.energy_prices['sell'],
            sold_energy=0.0,
            bought_energy=0.0
        )

    def reset(self):
        """
        Reset the grid module to its initial state.
        """
        return GridOutput(
            buy_price=self.energy_prices['buy'],
            sell_price=self.energy_prices['sell'],
            sold_energy=0.0,
            bought_energy=0.0
        )