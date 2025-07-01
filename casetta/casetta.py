import itertools
import random
from copy import deepcopy
from typing import SupportsFloat, Any

import gymnasium as gym
import numpy as np
from gymnasium.core import ActType, ObsType

from casetta.modules.building import Building
from casetta.modules.electric_battery import ElectricBattery
from casetta.modules.grid import Grid
from casetta.utils.common import merge_dataclasses, merge_box_spaces


class Casetta(gym.Env):
    """
    A smart building simulation environment with:
    - Building energy demand & internal conditions
    - Battery storage system
    - Grid interaction for buying/selling energy
    """

    def __init__(self):
        super().__init__()
        self.time_step = 5  # minutes

        self.config = {
            'time_step': self.time_step,
            'grid': {
                'buy_energy': 0.1,   # $/kWh
                'sell_energy': 0.05, # $/kWh
            },
            'electric_battery': {
                'capacity': 10.0,  # kWh
            },
            'building': {
                'max_power': 3.0
            }
        }

        # Initialize modules
        self.building = Building(self.config)
        self.battery = ElectricBattery(self.config)
        self.grid = Grid(self.config)

        self.observation_space = merge_box_spaces([
            self.building.observation_space,
            self.battery.observation_space,
            self.grid.observation_space
        ])
        self.action_space = merge_box_spaces([
            self.building.action_space,
            self.battery.action_space,
            self.grid.action_space
        ])
        self.action_names = list(itertools.chain(*[self.building.action_names, self.battery.action_names, self.grid.action_names]))
        self.state = None  # Holds the merged observation state

    def reset(self, seed=None, options=None) -> tuple[ObsType, dict[str, Any]]:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        # Reset each module
        building_state = self.building.reset()
        battery_state = self.battery.reset()
        grid_state = self.grid.reset()

        # Merge all states into a single unified observation dataclass
        self.state = merge_dataclasses(
            "State",
            [building_state, battery_state, grid_state]
        )
        return self.state, {}

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        assert self.state is not None, "Call `reset()` before `step()`."

        if not isinstance(action, dict):
            action = dict(zip(self.action_names, action))

        new_state = deepcopy(self.state)

        # Step through each module
        building_state = self.building.step(new_state, action)
        battery_state = self.battery.step(new_state, action)

        # Compute remaining unmet load (from house demand)
        load = building_state.non_shiftable_load
        remaining_load = max(load - battery_state.battery2house_energy, 0.0)

        # Energy exchange with grid
        grid2house_energy = remaining_load
        bought_energy = grid2house_energy + battery_state.grid2battery_energy
        sold_energy = battery_state.battery2grid_energy

        grid_state = self.grid.step(new_state, action)
        grid_state.bought_energy = bought_energy
        grid_state.sold_energy = sold_energy

        # Merge next state
        self.state = merge_dataclasses(
            "State",
            [building_state, battery_state, grid_state]
        )

        # Placeholder reward logic (zero reward)
        reward = 0.0
        terminated = False
        truncated = False
        info = {}

        return self.state, reward, terminated, truncated, info

