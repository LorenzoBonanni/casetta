import json
import random
from copy import deepcopy
from typing import SupportsFloat, Any

import gymnasium as gym
import numpy as np
from gymnasium.core import ActType, ObsType

from casetta.utils.modules_factory import create_modules


class Casetta(gym.Env):
    """
    A smart building simulation environment
    """

    def __init__(self, config_path: str):
        super().__init__()
        self.time_step = 5  # minutes
        # Initialize modules
        self.config = json.load(open(config_path))
        self.energy_exchange_manager = create_modules(self.config)

        self.observation_space = self.energy_exchange_manager.observation_space
        self.action_space = self.energy_exchange_manager.action_space
        self.action_names = self.energy_exchange_manager.action_names
        self.state = None  # Holds the merged observation state

    def reset(self, seed=None, options=None) -> tuple[ObsType, dict[str, Any]]:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        # Reset each module
        self.state = self.energy_exchange_manager.reset()
        return self.state, {}

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        assert self.state is not None, "Call `reset()` before `step()`."

        if not isinstance(action, dict):
            action = dict(zip(self.action_names, action))

        new_state = deepcopy(self.state)

        self.state = self.energy_exchange_manager.step(new_state, action)
        # Placeholder reward logic (zero reward)
        reward = 0.0
        terminated = False
        truncated = False
        info = {}

        return self.state, reward, terminated, truncated, info
