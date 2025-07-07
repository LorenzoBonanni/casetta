import abc

from casetta_env.modules.core.base_module import BaseModule


class EnergyProducer(BaseModule):

    @abc.abstractmethod
    def produce_electric_energy(self, percentage):
        """Output energy based on the given percentage of the maximum capacity."""
        pass