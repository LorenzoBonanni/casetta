class Grid:
    def __init__(self):
        self.energy_prices = {
            'buy': 0.15,  # $ per kWh
            'sell': 0.05   # $ per kWh
        }

    def next(self, current, action):
        sold_energy = action['sold_energy']
        bought_energy = action['bought_energy']

