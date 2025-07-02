import numpy as np
import gymnasium as gym

from casetta.modules.base_module import BaseModule
from casetta.utils.common import merge_dataclasses, merge_box_spaces

class EnergyExchangeManager(BaseModule):

    def __init__(self, energy_producers, energy_consumers, config):
        super().__init__(config)
        self.energy_producers = energy_producers
        self.energy_consumers = energy_consumers
        self.modules = {**energy_producers, **energy_consumers}

        self.action_names = []
        self.action_names_by_producer = {pname: [] for pname in energy_producers}
        self.action_names_by_consumer = {cname: [] for cname in energy_consumers}

        # Register all possible producer->consumer actions except producer==consumer
        for pname in self.energy_producers:
            for cname in self.energy_consumers:
                if cname != pname:
                    action_name = f"{pname}_to_{cname}"
                    self.action_names.append(action_name)
                    self.action_names_by_producer[pname].append(action_name)
                    self.action_names_by_consumer[cname].append(action_name)

        n_actions = len(self.action_names)
        self.action_space = gym.spaces.Box(
            low=np.zeros(n_actions, dtype=np.float32),
            high=np.ones(n_actions, dtype=np.float32)
        )
        self.observation_space = merge_box_spaces([
            module.observation_space for module in self.modules.values()
        ])

    def get_state(self):
        """
        Return merged state dataclass across all modules.
        """
        return merge_dataclasses(
            "State",
            [module.get_state() for module in self.modules.values()]
        )

    def reset(self):
        """
        Reset all modules and return merged initial state.
        """
        return merge_dataclasses(
            "State",
            [module.reset() for module in self.modules.values()]
        )

    def _rebalance_action(self, action):
        """
        Ensure producer actions sum to no more than 1.0 each.
        Returns a dictionary of rebalanced action values by action name.
        """
        rebalanced_action = {}
        for producer_name, action_names in self.action_names_by_producer.items():
            total = sum(action[name] for name in action_names)
            for name in action_names:
                rebalanced_action[name] = action[name] / total if total > 1.0 else action[name]
        return rebalanced_action

    def step(self, state, action):
        """
        Proceed one simulation step:
            * Rebalance and apply actions through modules
            * Transfer energy between producers and consumers as dictated by actions
        Returns merged new state.
        """
        action_rebalanced = self._rebalance_action(action)
        for module in self.modules.values():
            module.step(state, action_rebalanced)

        for action_name, value in action_rebalanced.items():
            if value > 0.0:
                producer_name, consumer_name = action_name.split('_to_')
                producer = self.energy_producers[producer_name]
                consumer = self.energy_consumers[consumer_name]
                produced_energy = producer.produce(percentage=value)
                consumer.consume(produced_energy)

        return self.get_state()