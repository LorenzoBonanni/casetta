import abc

from casetta_env.modules.core.base_module import BaseModule


class ThermalProducer(BaseModule):

    @abc.abstractmethod
    def produce_thermal_energy(self, percentage):
        """Output thermal energy based on the given percentage of the maximum capacity."""
        pass