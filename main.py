from casetta.casetta import Casetta

env = Casetta()
state, *_ = env.reset()

action = {'grid_to_electric_battery': 0.82,
          'grid_to_building': 0.56,
          'electric_battery_to_grid': 0.3,
          'electric_battery_to_building': 0.18}
s, *_ = env.step(action)
print("aaaa")
