class BaseModule:
    def __init__(self, config):
        self.config = config

    def reset(self):
        raise NotImplementedError

    def step(self, state, action):
        raise NotImplementedError
