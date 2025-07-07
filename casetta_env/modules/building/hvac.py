import numpy as np


import gymnasium as gym

from casetta_env.modules.core.energy_consumer import EnergyConsumer
from casetta_env.modules.core.thermal_consumer import ThermalConsumer
from casetta_env.utils.types import HvacOutput


class Hvac(EnergyConsumer, ThermalConsumer):
    def consume_thermal_energy(self, amount):
        self.consumed_thermal_energy += amount

    def __init__(self, config):
        super().__init__(config)
        self.power_rating = config['modules']['hvac']['power_rating']
        self.consumed_electric_energy = 0.0
        self.current_temp = 0.0
        self.set_point = 0.0
        self.consumed_thermal_energy = 0.0
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, -np.inf, 0.0]),
            high=np.array([np.inf, np.inf, np.inf]),
        )

    def consume_electric_energy(self, amount):
        self.consumed_electric_energy += amount

    def reset(self):
        """
        Reset the internal state and returns a fresh HvacOutput.
        """
        self.consumed_electric_energy = 0.0
        self.current_temp = 0.0
        self.set_point = 0.0
        self.consumed_thermal_energy = 0.0
        return HvacOutput(
            consumed_electric_energy=0.0,
            delta_temperature=0.0,
            consumed_thermal_energy=0.0
        )

    def step(self, state, action):
        """
        Update state with external conditions and resets consumed energy counter for the step.
        """
        self.consumed_electric_energy = 0.0
        self.current_temp = state.building_internal_temperature
        self.set_point = state.building_thermal_set_point

    def get_state(self):
        """
        Returns HvacOutput with current consumption and computed delta temperature.
        """
        direction = 1 if self.set_point >= self.current_temp else -1
        delta_temperature = self.consumed_electric_energy / self.power_rating

        return HvacOutput(
            consumed_electric_energy=self.consumed_electric_energy,
            delta_temperature=direction * delta_temperature,
            consumed_thermal_energy=self.consumed_thermal_energy
        )