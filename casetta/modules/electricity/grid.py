import gymnasium as gym
import numpy as np

from casetta.modules.core.energy_consumer import EnergyConsumer
from casetta.modules.core.energy_producer import EnergyProducer
from casetta.utils.types import GridOutput


class Grid(EnergyConsumer, EnergyProducer):
    def __init__(self, config):
        super().__init__(config)
        self.max_power = config['modules']['building']['max_power']  # Maximum power in kW
        self.energy_prices = {
            'buy': config['modules']['grid']['buy_energy'],  # $ per kWh
            'sell': config['modules']['grid']['sell_energy'],  # $ per kWh
        }
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([100.0, 100.0, np.inf, np.inf]),
        )
        self.state = None

    def _update_energy_prices(self, state):
        """
        Update the energy prices based on the current state of the environment.
        :param state: the current state of the environment
        :return:
        """
        pass

    def _reset_energy_prices(self):
        """
        Reset the energy prices to their initial values.
        :return:
        """
        pass

    def step(self, state, action) -> None:
        self._update_energy_prices(state)
        self.state = GridOutput(
            buy_price=self.energy_prices['buy'],
            sell_price=self.energy_prices['sell'],
            sold_energy=0.0,
            bought_energy=0.0
        )

    def consume(self, amount):
        """Sell energy to the grid."""
        self.state.sold_energy += amount

    def produce(self, percentage):
        """Buy energy from the grid based on the percentage of maximum power."""
        quantity = self.max_power * percentage  # kW
        self.state.bought_energy += quantity
        return quantity

    def get_state(self):
        return self.state

    def reset(self):
        """
        Reset the grid module to its initial state.
        """
        self._reset_energy_prices()
        return GridOutput(
            buy_price=self.energy_prices['buy'],
            sell_price=self.energy_prices['sell'],
            sold_energy=0.0,
            bought_energy=0.0
        )
