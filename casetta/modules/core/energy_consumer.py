import abc

from casetta.modules.core.base_module import BaseModule


class EnergyConsumer(BaseModule):

    @abc.abstractmethod
    def consume(self, amount):
        """Input a specified amount of energy."""
        pass