import json
import os
import random
from copy import deepcopy
from typing import SupportsFloat, Any

import gymnasium as gym
import numpy as np
from gymnasium.core import ActType, ObsType

from casetta_env.utils.common import merge_dataclasses, merge_box_spaces
from casetta_env.utils.modules_factory import create_modules


class Casetta(gym.Env):
    """
    A smart building simulation environment
    """

    def __init__(self, config_path = 'config/config.json'):
        super().__init__()
        cwd = os.getcwd()
        config_path = os.path.join(cwd, 'casetta_env/casetta', config_path)
        self.time_step = 5  # minutes
        # Initialize modules
        self.config = json.load(open(config_path))
        self.modules = create_modules(self.config)
        self.energy_exchange_manager = self.modules['energy_exchange']
        self.thermal_exchange_manager = self.modules['thermal_exchange']

        self.observation_space = merge_box_spaces([
            module.observation_space
            for module_name, module in self.modules.items() if 'exchange' not in module_name
        ])

        self.action_space = merge_box_spaces([
            self.energy_exchange_manager.action_space,
            self.thermal_exchange_manager.action_space,
            gym.spaces.Box(low=0, high=1)
        ])
        self.action_names = (self.energy_exchange_manager.action_names +
                             self.thermal_exchange_manager.action_names) + ['source']

        self.state = None  # Holds the merged observation state

    def reset(self, seed=None, options=None) -> tuple[ObsType, dict[str, Any]]:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        # Reset each module
        self.state = merge_dataclasses(
            "State",
            [module.reset() for module_name, module in self.modules.items() if 'exchange' not in module_name]
        )
        return self.state, {}

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        assert self.state is not None, "Call `reset()` before `step()`."

        if not isinstance(action, dict):
            action = dict(zip(self.action_names, action))

        new_state = deepcopy(self.state)
        for module_name, module in self.modules.items():
            if 'exchange' not in module_name:
                module.step(new_state, action)

        self.energy_exchange_manager.step(new_state, action)
        self.thermal_exchange_manager.step(new_state, action)
        self.state = merge_dataclasses(
            "State",
            [module.get_state() for module_name, module in self.modules.items() if 'exchange' not in module_name]
        )
        # self.state = self.energy_exchange_manager.step(new_state, action)
        # Placeholder reward logic (zero reward)
        reward = 0.0
        terminated = False
        truncated = False
        info = {}

        return self.state, reward, terminated, truncated, info
