class HeatPump:
    def __init__(self, power_rating=1000):
        self.power_rating = power_rating  # Power rating in Watts
        self.time_step = 5

    def compute_power_output(self, current, action):
        source = action['source']  # 'air', 'ground'
        ground_temperature = current['ground_temperature']
        air_temperature = current['external_temperature']
        input_temperature = ground_temperature if source == 0 else air_temperature
        return self.power_rating