import datetime
import itertools

import numpy as np

from casetta.modules.base_module import BaseModule
from casetta.utils.types import BuildingOutput
import gymnasium as gym

class Building(BaseModule):
    """
    Represents the building and its interaction with the environment and occupants.
    """

    DEFAULT_TEMP_SETPOINT = 22.0  # °C
    DEFAULT_LOAD = 2  # KWh
    DEFAULT_INTERNAL_TEMP = 20.0  # °C

    def __init__(self, config):
        """
        Initializes the Building module with simulation time step and temperature profiles.

        Args:
            config (dict): Contains 'time_step' in minutes.
        """
        super().__init__(config)
        self.time_step = config['time_step']
        self.max_power = config['building']['max_power']
        self.temperature_set_point = self.DEFAULT_TEMP_SETPOINT

        self.hours = list(range(24))
        self.irradiance_profile = self._generate_irradiance_profile()
        self.external_temperature_profile = self._generate_external_temperature_profile()
        self.ground_temperature_profile = self._generate_ground_temperature_profile()
        self.dhw_profile = self._generate_dhw_profile()
        self.current_datetime = None
        self.internal_temperature = None
        self.action_space = gym.spaces.Box(
            low=np.array([]),
            high=np.array([]),
        )
        self.action_names = []
        min_date = datetime.date.min
        max_date = datetime.date.max
        min_time = datetime.time.min
        max_time = datetime.time.max
        self.observation_space = gym.spaces.Box(
            low = np.array([
                0.0,    # non_shiftable_load
                0.0,    # internal_temperature
                -50.0,  # external_temperature
                5.0,    # ground_temperature
                0.0,    # solar_irradiation
                0.0,    # thermal_set_point
                0,      # weekday
                min_date.day,      # day
                min_date.month,      # month
                min_date.year,  # year
                min_time.hour,      # hour
                min_time.minute,      # minute
                0.0     # domestic_hot_water_request
            ]),
            high=np.array([
                self.max_power, # non_shiftable_load
                50.0, # internal temperature
                50.0, # external_temperature
                20.0, # ground_temperature
                1000.0, # solar_irradiation
                30, # thermal_set_point
                6,  # weekday
                max_date.day, # day
                max_date.month, # month
                max_date.year, # year
                max_time.hour, # hour
                max_time.minute, # minute
                100 # domestic_hot_water_request
            ]),
        )

    def _generate_irradiance_profile(self):
        return [max(0, np.sin(np.pi * (h - 6) / 12)) * 800 for h in self.hours]

    def _generate_external_temperature_profile(self):
        return [10 + 10 * np.sin(np.pi * (h - 6) / 12) for h in self.hours]

    def _generate_ground_temperature_profile(self):
        return [15 + 5 * np.sin(np.pi * (h - 6) / 12) for h in self.hours]

    def _generate_dhw_profile(self):
        usage = [0] * 24
        usage[6:9] = [20, 30, 25]                      # Morning peak
        usage[9:17] = [5, 3, 6, 4, 3, 6, 3, 6]         # Daytime low
        usage[18:21] = [25, 35, 30]                    # Evening peak
        usage[21:] = [3, 3, 1]                         # Night
        usage[0:6] = [1, 1, 0, 1, 1, 1]                # Early morning
        return usage

    def update_internal_temperature(self, internal_temp, external_temp):
        """
        Naive thermal dynamics simulation.

        Args:
            internal_temp (float): Internal temperature [°C].
            external_temp (float): External temperature [°C].

        Returns:
            float: New internal temperature [°C].
        """
        direction = 1 if internal_temp < external_temp else -1
        delta = abs(external_temp - internal_temp) * 0.1  # Scaling factor
        return internal_temp + direction * delta

    def step(self, state, action) -> BuildingOutput:
        """
        Advances the building simulation by one time step.

        Args:
            state: The current state of the building.
            action: The action to be applied at this step.

        Returns:
            BuildingOutput: The output data for the current time step, including temperatures, loads, and other relevant parameters.
        """
        date = datetime.datetime(
            state.year, state.month, state.day,
            state.hour, state.minute
        ) + datetime.timedelta(minutes=self.time_step)

        hour = date.hour

        external_temp = self.external_temperature_profile[hour]
        internal_temp = self.update_internal_temperature(state.internal_temperature, external_temp)

        return BuildingOutput(
            # non_shiftable_load=(self.DEFAULT_LOAD / 60) * self.time_step,
            non_shiftable_load=self.DEFAULT_LOAD,
            internal_temperature=internal_temp,
            external_temperature=external_temp,
            ground_temperature=self.ground_temperature_profile[hour],
            solar_irradiation=self.irradiance_profile[hour],
            thermal_set_point=self.temperature_set_point,
            weekday=date.weekday(),
            day=date.day,
            month=date.month,
            year=date.year,
            hour=hour,
            minute=date.minute,
            domestic_hot_water_request=self.dhw_profile[hour],
        )

    def reset(self) -> BuildingOutput:
        """
        Resets the building environment to an initial state.

        Returns:
            BuildingOutput: Initial output after reset.
        """
        self.current_datetime = datetime.datetime(2010, 1, 1, 0, 0)
        self.internal_temperature = self.DEFAULT_INTERNAL_TEMP

        hour = self.current_datetime.hour

        return BuildingOutput(
            # non_shiftable_load=(self.DEFAULT_LOAD / 60) * self.time_step,
            non_shiftable_load=self.DEFAULT_LOAD,
            internal_temperature=self.internal_temperature,
            external_temperature=self.external_temperature_profile[hour],
            ground_temperature=self.ground_temperature_profile[hour],
            solar_irradiation=self.irradiance_profile[hour],
            thermal_set_point=self.temperature_set_point,
            weekday=self.current_datetime.weekday(),
            day=self.current_datetime.day,
            month=self.current_datetime.month,
            year=self.current_datetime.year,
            hour=self.current_datetime.hour,
            minute=self.current_datetime.minute,
            domestic_hot_water_request=self.dhw_profile[hour],
        )