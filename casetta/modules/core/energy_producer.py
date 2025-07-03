import abc

from casetta.modules.core.base_module import BaseModule


class EnergyProducer(BaseModule):

    @abc.abstractmethod
    def produce(self, percentage):
        """Output energy based on the given percentage of the maximum capacity."""
        pass