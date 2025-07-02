import abc


class BaseModule(abc.ABC):
    def __init__(self, config):
        self.config = config
        self.action_space = None
        self.observation_space = None
        self.action_names = []

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def step(self, state, action):
        pass

    @abc.abstractmethod
    def get_state(self):
        pass

class EnergyConsumer(BaseModule):

    @abc.abstractmethod
    def consume(self, amount):
        """Input a specified amount of energy."""
        pass

class EnergyProducer(BaseModule):

    @abc.abstractmethod
    def produce(self, percentage):
        """Output energy based on the given percentage of the maximum capacity."""
        pass