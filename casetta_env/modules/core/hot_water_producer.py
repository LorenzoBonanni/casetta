import abc

from casetta_env.modules.core.base_module import BaseModule


class HotWaterProducer(BaseModule):
    @abc.abstractmethod
    def produce_hot_water(self, percentage):
        """Output hot water based on the given percentage of the maximum capacity."""
        pass