from casetta.modules.base_module import BaseModule
from casetta.utils.types import PhotovoltaicOutput
import gymnasium as gym

class PhotovoltaicPanel(BaseModule):
    def __init__(self, config):
        super().__init__(config)
        self.num_modules = config['photovoltaic']['num_modules'] # Number of modules
        self.wp = config['photovoltaic']['rated_power']  # Rated power in Wp (Watts peak)
        self.time_step = config['time_step']  # Time step in minutes

        self.observation_space = gym.spaces.Box(
            low=0.0,
            high=float('inf')
        )
        # self.action_space = gym.spaces.Box(
        #     low=0.0,
        #     high=float('inf')
        # )

    def step(self, current, action) -> PhotovoltaicOutput:
        """
        Compute the power output based on current irradiance.
        """
        irradiance = current['irradiance']
        power_output = irradiance * self.wp * self.num_modules / 1000  # kW
        energy_produced = power_output * (self.time_step / 60)  # kWh
        return PhotovoltaicOutput(
            energy_produced=energy_produced
        )

    def reset(self):
        """
        Reset the photovoltaic panel module to its initial state.
        """
        pass