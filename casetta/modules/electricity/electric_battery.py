import numpy as np
import gymnasium as gym

from casetta.modules.core.energy_consumer import EnergyConsumer
from casetta.modules.core.energy_producer import EnergyProducer
from casetta.utils.types import ElectricBatteryOutput


class ElectricBattery(EnergyProducer, EnergyConsumer):
    """
    Represents an electric battery module for energy storage and dispatch.
    """

    def get_state(self):
        # Update stored_energy based on accumulated charged/discharged energy
        # This is where the stored_energy actually changes.
        self.stored_energy += self.state.charged_energy - self.state.discharged_energy

        # Ensure stored_energy stays within valid bounds (0 to capacity)
        self.stored_energy = np.clip(self.stored_energy, 0, self.capacity)

        # Calculate SoC based on the updated stored_energy
        self.soc = self.stored_energy / self.capacity

        return ElectricBatteryOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            charged_energy=self.state.charged_energy,  # Return accumulated charged energy for this step
            discharged_energy=self.state.discharged_energy  # Return accumulated discharged energy for this step
        )

    def __init__(self, config):
        super().__init__(config)
        self.capacity = config['modules']['electric_battery']['capacity']  # in kWh
        self.soc = 0.0
        self.stored_energy = 0.0
        self.state = ElectricBatteryOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            charged_energy=0.0,
            discharged_energy=0.0
        )
        self.reset()
        self.observation_space = gym.spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([1.0, self.capacity, np.inf, np.inf])
        )

    def reset(self):
        self.stored_energy = 0.0  # in kWh
        self.soc = 0.0  # State of Charge (0 to 1)
        # Reset the state to reflect initial conditions
        self.state = ElectricBatteryOutput(
            soc=self.soc,
            stored_energy=self.stored_energy,
            charged_energy=0.0,
            discharged_energy=0.0
        )
        return self.state

    def produce_electric_energy(self, percentage):
        # Calculate amount to discharge based on current stored_energy
        # This operation doesn't change self.stored_energy directly
        amount_to_discharge = self.stored_energy * percentage

        # Accumulate discharged energy in the state for the current step
        self.state.discharged_energy += amount_to_discharge

        return amount_to_discharge if self.stored_energy > 0 else 0.0

    def consume_electric_energy(self, amount):
        # Accumulate charged energy in the state for the current step
        # Ensure we don't try to charge more than remaining capacity
        self.state.charged_energy += min(amount, self.capacity - self.stored_energy - self.state.charged_energy)

    def step(self, state, action):
        # The `state` parameter here represents the state *before* this step's actions
        self.state = ElectricBatteryOutput(
            soc=state.electricbattery_soc,
            stored_energy=state.electricbattery_stored_energy,
            charged_energy=0.0,  # Reset charged energy for the new step
            discharged_energy=0.0  # Reset discharged energy for the new step
        )
        self.stored_energy = state.electricbattery_stored_energy
