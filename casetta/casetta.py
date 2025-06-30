from typing import SupportsFloat, Any

import gymnasium as gym
from gymnasium.core import ActType, ObsType

from casetta.modules.building import Building


class Casetta(gym.Env):
    def __init__(self):
        self.building = None  # Placeholder for building object
        self.grid = None
        self.time_step = 5  # Time step in minutes
        self.state = {
            'index': 0,
            'non_shiftable_load': 0.0,
            'internal_temperature': 20.0,
            'external_temperature': 15.0,
            'ground_temperature': 10.0,
            'solar_irradiation': 500.0,
            'thermal_set_point': 22.0,
            'weekday': 0,
            'day': 1,
            'month': 1,
            'year': 2020,
            'hour': 0,
            'minute': 0,
            'domestic_hot_water_request': 0.0,
            'energy_price': 0.1,
            'total_energy_consumption': 0.0,
            'total_energy_production': 0.0,
            'percentage_of_energy_consumption_from_grid': 0.0,
            'percentage_dhw_soc': 0.0,
            'percentage_ctes_soc': 0.0,
            'percentage_hes_soc': 0.0,
            'percentage_battery_soc': 0.0,
        }
        self.building = Building(self.time_step)

    def step(self, action: ActType) -> tuple[dict, SupportsFloat, bool, bool, dict[str, Any]]:
        new_state = self.state.copy()
        new_state['index'] += 1
        self.building
        new_state[]

        return self.state, 0.0, False, False, {}