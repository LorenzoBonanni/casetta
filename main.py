from casetta.casetta import Casetta

env = Casetta()
state, *_ = env.reset()

action = env.action_space.sample()
env.step(action)
print("aaa")