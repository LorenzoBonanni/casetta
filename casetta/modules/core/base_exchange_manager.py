import abc
from abc import ABC

import gymnasium as gym
import numpy as np


class BaseExchangeManager(ABC):
    def __init__(self, producers, consumers, prefix=""):
        self.producers = producers
        self.consumers = consumers
        self.modules = {**producers, **consumers}
        self.prefix = prefix
        self.action_names = []
        self.action_names_by_producer = {pname: [] for pname in producers}
        self.action_names_by_consumer = {cname: [] for cname in consumers}

        for pname in producers:
            for cname in consumers:
                if pname != cname:
                    action_name = f"{self.prefix}_{pname}_to_{cname}"
                    self.action_names.append(action_name)
                    self.action_names_by_producer[pname].append(action_name)
                    self.action_names_by_consumer[cname].append(action_name)

        n_actions = len(self.action_names)
        self.action_space = gym.spaces.Box(
            low=np.zeros(n_actions, dtype=np.float32),
            high=np.ones(n_actions, dtype=np.float32)
        )

    def _rebalance_action(self, action):
        rebalanced = {}
        for producer, names in self.action_names_by_producer.items():
            total = sum(action[name] for name in names)
            for name in names:
                rebalanced[name] = action[name] / total if total > 1.0 else action[name]

        return rebalanced

    @abc.abstractmethod
    def consume_callback(self, consumer, produced):
        pass

    @abc.abstractmethod
    def produce_callback(self, producer, value):
        pass

    def step(self, state, action):
        action_rebalanced = self._rebalance_action(action)
        for name, value in action_rebalanced.items():
            if value > 0.0 and "_to_" in name:
                name = name[len(self.prefix) + 1:]
                producer_name, consumer_name = name.split('_to_')
                producer = self.producers[producer_name]
                consumer = self.consumers[consumer_name]
                produced = self.produce_callback(producer, value)
                self.consume_callback(consumer, produced)