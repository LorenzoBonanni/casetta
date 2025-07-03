import abc

from casetta.modules.core.base_module import BaseModule


class ThermalConsumer(BaseModule):

    @abc.abstractmethod
    def consume_thermal_energy(self, amount):
        """Input a specified amount of thermal energy."""
        pass