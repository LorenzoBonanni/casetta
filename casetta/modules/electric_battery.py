class ElectricBattery:
    """
    Class representing an electric battery with a specific capacity.
    """

    def __init__(self, capacity: float):
        """
        Initialize the ElectricBattery with a given capacity.

        :param capacity: The capacity of the battery in kWh.
        """
        self.capacity = capacity
        self.stored_energy = 0.0
        self.soc = 0.0

    def fill(self, energy):
        """
        Fill the battery with energy.

        :param energy: Energy in kWh to fill the battery.
        """
        if energy < 0:
            raise ValueError("Energy to fill must be non-negative.")
        self.stored_energy += energy
        if self.stored_energy > self.capacity:
            self.stored_energy = self.capacity
        self.soc = self.stored_energy / self.capacity
        return self.soc

    def discharge(self, amount):
        """
        Discharge the battery.

        :param amount: Amount of energy to discharge in kWh.
        :return: The state of charge after discharging.
        """
        if amount < 0:
            raise ValueError("Amount to discharge must be non-negative.")
        self.stored_energy -= amount
        if self.stored_energy < 0:
            self.stored_energy = 0
        self.soc = self.stored_energy / self.capacity
        return self.soc