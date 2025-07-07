import abc

from casetta_env.modules.core.base_module import BaseModule


class EnergyConsumer(BaseModule):

    @abc.abstractmethod
    def consume_electric_energy(self, amount):
        """Input a specified amount of energy."""
        pass