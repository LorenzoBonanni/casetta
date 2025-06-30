class Hvac:
    def __init__(self, power_rating=1000, efficiency=0.9, time_step=5):
        """
        Initializes the HVAC system with a power rating and efficiency.

        :param power_rating: Power rating of the HVAC system in Watts.
        :param efficiency: Efficiency of the HVAC system (0 to 1).
        """
        self.power_rating = power_rating
        self.efficiency = efficiency
        self.time_step = time_step

    def compute_energy_and_temperature(self, current, action):
        """
        Computes the energy consumption and new delta temperature after running the HVAC.
        """

        current_temp = current['internal_temperature']
        setpoint = action['setpoint']

        if current_temp == setpoint:
            return 0.0, current_temp

        # TODO: Handle power rating based on action if needed
        power_rating = self.power_rating

        # Convert time_step from minutes to hours
        duration_hours = self.time_step / 60.0

        # Assume HVAC changes temp at a rate proportional to power and efficiency
        temp_change_rate = power_rating * self.efficiency / 10000  # °C per hour (arbitrary scaling)
        direction = 1 if setpoint > current_temp else -1
        temp_diff = abs(setpoint - current_temp)
        possible_temp_change = temp_change_rate * duration_hours

        actual_temp_change = min(temp_diff, possible_temp_change)
        delta_temp = direction * actual_temp_change

        # Energy consumed in kWh
        energy_consumed = (power_rating * duration_hours) / 1000 if actual_temp_change > 0 else 0.0

        return energy_consumed, delta_temp