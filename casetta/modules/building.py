import datetime

import numpy as np

from casetta.utils.types import BuildingOutput


class Building:
            """
            Represents the building itself. It provides data on external conditions, user behavior
            (e.g., temperature set-points, energy demands), and temporal information.

            It should return the following data:
            - Requested Energy [kW] – Energy requested by home appliances (e.g., dishwasher)
            - Internal Temperature [°C] – Current internal building temperature
            - External Temperature [°C] – Outdoor temperature
            - Ground Temperature [°C] – Temperature of Ground Water
            - Solar Irradiation [W/m²] – Solar power per unit area
            - Thermal Set Point [°C] – Desired internal temperature set by the user
            - Weekday, Day, Month, Year, Hour, Minute – Date and time information
            - Domestic Hot Water Request– Amount of Hot Water requested by the House
            """

            def __init__(self, time_step=5):
                """
                Initializes the Building with a given time step in minutes.

                Args:
                    time_step (int): The simulation time step in minutes.
                """
                self.time_step = time_step
                self.hours = range(24)

                # Generate a sample irradiance profile (sinusoidal between 6h and 18h).
                self.irradiance_profile = [max(0, np.sin(np.pi * (h - 6) / 12)) * 800 for h in self.hours]
                # Generate a sample external temperature profile
                self.external_temperature_profile = [10 + 10 * np.sin(np.pi * (h - 6) / 12) for h in self.hours]
                self.ground_temperature_profile = [15 + 5 * np.sin(np.pi * (h - 6) / 12) for h in self.hours]
                self.dhw_profile = self.get_dhw_profile()
                self.temperature_set_point = 22.0  # Default thermal set point in °C

            def get_dhw_profile(self):
                """
                Simulates naive domestic hot water (DHW) usage over a 24-hour period.

                Returns:
                    list: Array of hourly hot water usage (liters/hour).
                """
                usage = [0 for h in self.hours]

                # Morning peak: 6–9 AM
                usage[6:9] = [20, 30, 25]

                # Daytime low use: 9 AM – 5 PM
                usage[9:17] = [5, 3, 6, 4, 3, 6, 3, 6]

                # Evening peak: 6–9 PM
                usage[18:21] = [25, 35, 30]

                # Nighttime low use: rest of the hours remain at 0 or minimal
                usage[21:] = [3, 3, 1]
                usage[0:6] = [1, 1, 0, 1, 1, 1]

                return usage

            def update_internal_temperature(self, internal_temperature, external_temperature):
                """
                Update the internal temperature based on external and ground temperatures.
                This is a placeholder function and should be replaced with actual logic.

                Args:
                    internal_temperature (float): Current internal temperature in °C.
                    external_temperature (float): Current external temperature in °C.

                Returns:
                    float: Updated internal temperature in °C.
                """
                sign = 1 if internal_temperature < external_temperature else -1
                delta_temp = abs(external_temperature - internal_temperature) * 0.1  # Arbitrary scaling factor
                new_internal_temperature = internal_temperature + sign * delta_temp
                return new_internal_temperature

            def next(self, current) -> BuildingOutput:
                """
                Advances the building simulation by one time step and returns the updated state.

                Args:
                    current: An object with current simulation state attributes (year, month, day, hour, minute, internal_temperature).

                Returns:
                    BuildingOutput: The updated building state for the next time step.
                """
                date = datetime.datetime(current.year, current.month, current.day, current.hour, current.minute)
                date += datetime.timedelta(minutes=self.time_step)
                weekday = date.weekday()
                # Assume a constant hourly load, e.g., 2000 Wh per hour.
                load = 2000  # Wh
                external_temperature = self.external_temperature_profile[date.hour]
                internal_temperature = self.update_internal_temperature(current.internal_temperature, external_temperature)
                ground_temperature = self.ground_temperature_profile[date.hour]
                irradiance = self.irradiance_profile[date.hour]
                thermal_set_point = self.temperature_set_point
                domestic_hot_water = self.dhw_profile[date.hour]

                return BuildingOutput(
                    non_shiftable_load=(load / 60) * self.time_step,
                    internal_temperature=internal_temperature,
                    external_temperature=external_temperature,
                    ground_temperature=ground_temperature,
                    solar_irradiation=irradiance,
                    thermal_set_point=thermal_set_point,
                    weekday=weekday,
                    day=date.day,
                    month=date.month,
                    year=date.year,
                    hour=date.hour,
                    minute=date.minute,
                    domestic_hot_water_request=domestic_hot_water,
                )