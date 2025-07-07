import abc

from casetta_env.modules.core.base_module import BaseModule


class HotWaterConsumer(BaseModule):
    @abc.abstractmethod
    def consume_hot_water(self, percentage):
        """Output hot water based on the given percentage of the maximum capacity."""
        pass