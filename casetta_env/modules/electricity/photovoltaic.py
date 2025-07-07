import gymnasium as gym

from casetta_env.modules.core.energy_producer import EnergyProducer
from casetta_env.utils.types import PhotovoltaicOutput


class PhotovoltaicPanel(EnergyProducer):

    def produce_electric_energy(self, percentage):
        irradiation = self.irradiation
        power_output = (irradiation / 1000) * self.wp * self.num_modules   # kW
        out = percentage * power_output
        self.produced_energy += out
        return out

    def get_state(self):
        return PhotovoltaicOutput(
            energy_produced=self.produced_energy
        )

    def __init__(self, config):
        super().__init__(config)
        self.num_modules = config['modules']['photovoltaic']['num_modules'] # Number of modules
        self.wp = config['modules']['photovoltaic']['rated_power']  # Rated power in KWp
        self.time_step = config['time_step']  # Time step in minutes
        self.irradiation = None
        self.observation_space = gym.spaces.Box(
            low=0.0,
            high=float('inf')
        )
        self.produced_energy = 0.0  # Initialize produced energy

    def step(self, state, action) -> None:
        self.irradiation = state.building_solar_irradiation
        self.produced_energy = 0.0


    def reset(self):
        """
        Reset the photovoltaic panel module to its initial state.
        """
        return PhotovoltaicOutput(
            energy_produced=0.0
        )