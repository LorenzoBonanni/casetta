class HotThermalEnergyStorage:
    def __init__(self, capacity: float, efficiency: float):
        """
        Initialize the hot thermal energy storage system.

        :param capacity: Maximum energy storage capacity in kWh.
        :param efficiency: Efficiency of the storage system (0 to 1).
        """
        self.capacity = capacity
        self.efficiency = efficiency
        self.soc = 0.0
        self.current_energy = 0.0  # Current stored energy in kWh

    def store_energy(self, energy: float) -> None:
        """
        Store energy in the system.

        :param energy: Amount of energy to store in kWh.
        """
        if energy < 0:
            raise ValueError("Energy to store must be non-negative.")
        self.current_energy = min(self.capacity, self.current_energy + energy)
        self.soc = self.current_energy / self.capacity

    def retrieve_energy(self, energy: float) -> float:
        """
        Retrieve energy from the system.

        :param energy: Amount of energy to retrieve in kWh.
        :return: Amount of energy actually retrieved in kWh.
        """
        if energy < 0:
            raise ValueError("Energy to retrieve must be non-negative.")

        retrieved_energy = min(energy, self.current_energy * self.efficiency)
        self.current_energy -= retrieved_energy / self.efficiency
        self.soc = self.current_energy / self.capacity
        return retrieved_energy