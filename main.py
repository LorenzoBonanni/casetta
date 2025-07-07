from casetta_env.casetta.casetta import Casetta
env = Casetta()
initial_state, *_ = env.reset()

action = env.action_space.sample()
state, reward, terminated, truncated, info = env.step(action)
print(state)
