from casetta.casetta import Casetta


env = Casetta('casetta/config/config.json')
state, *_ = env.reset()

action = env.action_space.sample()
s, *_ = env.step(action)
