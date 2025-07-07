from casetta.casetta import Casetta


env = Casetta('casetta/config/config.json')
initial_state, *_ = env.reset()

action = env.action_space.sample()
state, reward, terminated, truncated, info = env.step(action)
