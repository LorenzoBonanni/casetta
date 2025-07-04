import numpy as np
import gymnasium as gym
from casetta.modules.core.thermal_consumer import ThermalConsumer
from casetta.modules.core.thermal_producer import ThermalProducer
from casetta.utils.types import ThermalEnergyStorageOutput


class ThermalEnergyStorage(ThermalConsumer, ThermalProducer):
    """
    Class representing a thermal energy storage system.
    """

    def consume_thermal_energy(self, amount):
        self.state.charged_energy += min(amount, self.capacity - self.stored_energy - self.state.charged_energy)

    def produce_thermal_energy(self, percentage):
        # Calculate amount to discharge based on current stored_energy
        # This operation doesn't change self.stored_energy directly
        amount_to_discharge = self.stored_energy * percentage

        # Accumulate discharged energy in the state for the current step
        self.state.discharged_energy += amount_to_discharge

        return amount_to_discharge

    def reset(self):
        self.stored_energy = 0.0  # in kJ
        self.soc = 0.0  # State of Charge (0 to 1)
        # Reset the state to reflect initial conditions
        self.state = ThermalEnergyStorageOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            charged_energy=0.0,
            discharged_energy=0.0
        )
        return self.state

    def step(self, state, action):
        self.state = ThermalEnergyStorageOutput(
            soc=state.thermalenergystorage_soc,
            stored_energy=state.thermalenergystorage_stored_energy,
            charged_energy=0.0,  # Reset charged energy for the new step
            discharged_energy=0.0  # Reset discharged energy for the new step
        )
        self.stored_energy = state.thermalenergystorage_stored_energy

    def get_state(self):
        self.stored_energy += self.state.charged_energy - self.state.discharged_energy

        # Ensure stored_energy stays within valid bounds (0 to capacity)
        self.stored_energy = np.clip(self.stored_energy, 0, self.capacity)

        # Calculate SoC based on the updated stored_energy
        self.soc = self.stored_energy / self.capacity

        return ThermalEnergyStorageOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            charged_energy=self.state.charged_energy,  # Return accumulated charged energy for this step
            discharged_energy=self.state.discharged_energy  # Return accumulated discharged energy for this step
        )

    def __init__(self, config):
        super().__init__(config)
        self.capacity = config['modules']['thermal_storage']['capacity'] # kJ
        self.stored_energy = 0.0
        self.soc = 0.0
        self.state = None
        self.state = ThermalEnergyStorageOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            charged_energy=0.0,
            discharged_energy=0.0
        )
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([1.0, self.capacity, np.inf, np.inf])
        )