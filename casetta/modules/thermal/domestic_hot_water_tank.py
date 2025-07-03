class DomesticHotWaterTank:
    def __init__(self):
        self.soc = 0.0  # State of charge (0 to 1)

    def fill(self, energy):
        """
        Fill the tank with energy.
        :param energy: Energy in kWh to fill the tank.
        """
        # Convert energy to liters (assuming 1 kWh heats 1 liter of water by 1°C)
        self.soc += energy * 1000 / (4.186 * 1)

    def discharge(self, amount):
        """
        Discharge the tank.
        """
        if self.soc > 0:
            self.soc = max(0, self.soc - amount)
            return self.soc