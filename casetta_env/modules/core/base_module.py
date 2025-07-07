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
