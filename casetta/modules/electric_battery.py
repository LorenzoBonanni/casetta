import numpy as np

from casetta.modules.base_module import BaseModule
from casetta.utils.types import ElectricBatteryOutput
import gymnasium as gym

class ElectricBattery(BaseModule):
    """
    Represents an electric battery module for energy storage and dispatch.
    """

    def __init__(self, config):
        super().__init__(config)
        self.capacity = config['electric_battery']['capacity']  # in kWh
        self.action_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0]),  # grid2battery, battery2house, battery2grid
            high=np.array([1.0, 1.0, 1.0]),  # normalized percentages (0 to 1)
        )
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),  # soc, stored_energy. battery2house_energy, battery2grid_energy, grid2battery_energy
            high=np.array([1.0, self.capacity, self.capacity, self.capacity, self.capacity]),
        )
        self.action_names = ['grid2battery', 'battery2house', 'battery2grid']
        self.reset()

    def reset(self):
        self.stored_energy = 0.0  # in kWh
        self.soc = 0.0            # State of Charge (0 to 1)
        return ElectricBatteryOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            battery2house_energy=0.0,
            battery2grid_energy=0.0,
            grid2battery_energy=0.0
        )

    def step(self, state, action) -> ElectricBatteryOutput:
        # Extract actions
        charge_pct = action.get('grid2battery', 0.0)
        discharge_house_pct = action.get('battery2house', 0.0)
        discharge_grid_pct = action.get('battery2grid', 0.0)

        # Normalize discharge percentages if they exceed 100%
        total_discharge_pct = discharge_house_pct + discharge_grid_pct
        if total_discharge_pct > 1.0:
            discharge_house_pct /= total_discharge_pct
            discharge_grid_pct /= total_discharge_pct

        # Compute discharges
        battery2house_energy = self.stored_energy * discharge_house_pct
        battery2grid_energy = self.stored_energy * discharge_grid_pct
        total_discharge = battery2house_energy + battery2grid_energy

        # Update stored energy
        self.stored_energy = max(self.stored_energy - total_discharge, 0.0)

        # Add energy from grid
        grid2battery_energy = self.capacity * charge_pct
        self.stored_energy = min(self.stored_energy + grid2battery_energy, self.capacity)

        # Update state of charge
        self.soc = self.stored_energy / self.capacity

        return ElectricBatteryOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            battery2house_energy=battery2house_energy,
            battery2grid_energy=battery2grid_energy,
            grid2battery_energy=grid2battery_energy
        )