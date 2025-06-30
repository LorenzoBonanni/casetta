class PhotovoltaicPanel:
    def __init__(self, num_modules=8, wp=420):
        self.num_modules = num_modules
        self.wp = wp  # Rated power (Wp) per module
        self.time_step = 5  # Time step in minutes

    def power_output(self, irradiance):
        """
        Calculate the output power in Watts.
        Irradiance is scaled relative to 1000 W/m².
        """
        total_rating = self.wp * self.num_modules
        return total_rating * (irradiance / 1000)