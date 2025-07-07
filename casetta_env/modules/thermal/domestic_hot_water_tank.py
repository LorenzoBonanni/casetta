import numpy as np


import gymnasium as gym

from casetta_env.modules.core.hot_water_producer import HotWaterProducer
from casetta_env.modules.core.thermal_consumer import ThermalConsumer
from casetta_env.utils.types import DomesticHotWaterTankOutput


class DomesticHotWaterTank(ThermalConsumer, HotWaterProducer):
    def consume_thermal_energy(self, amount):
        charged_water = self._thermal_energy_to_liters(self.state.charged_energy)
        self.state.charged_energy += min(amount, self.capacity - self.stored_water - charged_water)

    def _thermal_energy_to_liters(self, energy_kJ):
        # Assuming 1 liter of water requires 4.186 kJ to raise by 1°C (specific heat capacity)
        # If you know the temperature difference (delta_T), you can convert kJ to liters:
        # liters = charged_energy / (4.186 * delta_T)
        delta_T = 50  # Change as needed
        charged_liters = energy_kJ / (4.186 * delta_T)
        return charged_liters

    def reset(self):
        self.stored_water = 0.0  # in kJ
        self.soc = 0.0  # State of Charge (0 to 1)
        # Reset the state to reflect initial conditions
        self.state = DomesticHotWaterTankOutput(
            soc=self.soc,
            stored_water=self.stored_water,
            charged_energy=0.0,  # Reset charged water for the new step
            discharged_water=0.0  # Reset discharged water for the new step
        )
        return self.state

    def step(self, state, action):
        self.state = DomesticHotWaterTankOutput(
            soc=state.domestichotwatertank_soc,
            stored_water=state.domestichotwatertank_stored_water,
            charged_energy=0.0,  # Reset charged energy for the new step
            discharged_water=0.0  # Reset discharged energy for the new step
        )
        self.stored_water = state.domestichotwatertank_stored_water

    def get_state(self):
        self.stored_water += self._thermal_energy_to_liters(self.state.charged_energy) - self.state.discharged_water

        # Ensure stored_energy stays within valid bounds (0 to capacity)
        self.stored_water = np.clip(self.stored_water, 0, self.capacity)

        # Calculate SoC based on the updated stored_energy
        self.soc = self.stored_water / self.capacity

        return DomesticHotWaterTankOutput(
            soc=self.soc,
            stored_water=self.stored_water,
            charged_energy=0.0,  # Reset charged water for the new step
            discharged_water=0.0  # Reset discharged water for the new step
        )

    def produce_hot_water(self, percentage):
        amount_to_discharge = self.stored_water * percentage
        self.discharged_water += amount_to_discharge

        return amount_to_discharge

    def __init__(self, config):
        super().__init__(config)
        self.state = None
        self.soc = 0.0  # State of charge (0 to 1)
        self.stored_water = 0.0
        self.charged_energy = 0.0
        self.discharged_water = 0.0
        self.capacity = config['modules']['dhw_tank']['capacity']  # in L
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([1.0, self.capacity, np.inf, np.inf]),
        )