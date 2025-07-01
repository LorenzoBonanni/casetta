from casetta.modules.base_module import BaseModule


class PhotovoltaicPanel(BaseModule):
    def __init__(self, config):
        super().__init__(config)
        self.num_modules = config['photovoltaic']['num_modules'] # Number of modules
        self.wp = config['photovoltaic']['rated_power']  # Rated power in Wp (Watts peak)
        self.time_step = config['time_step']  # Time step in minutes

    def step(self, current, action):
        """
        Compute the power output based on current irradiance.
        """
        irradiance = current['irradiance']

        power_output = irradiance * self.wp * self.num_modules / 1000  # kW
        energy_produced = power_output * (self.time_step / 60)  # kWh
        return energy_produced

    def reset(self):
        """
        Reset the photovoltaic panel module to its initial state.
        """
        pass