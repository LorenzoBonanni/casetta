from casetta.modules.core.energy_consumer import EnergyConsumer
from casetta.utils.types import HeatPumpOutput


# TODO: add thermal producer
class HeatPump(EnergyConsumer):
    def consume(self, amount):
        pass

    def reset(self):
        return HeatPumpOutput(
            consumed_electric_energy=0.0,
            produced_thermal_energy=0.0
        )

    def step(self, state, action):
        source = round(action['source'])  # 'air', 'ground'
        ground_temperature = state.building_ground_temperature
        air_temperature = state.builing_air_temperature
        self.input_temperature = ground_temperature if source == 0 else air_temperature

    def get_state(self):
        pass

    def __init__(self, config):
        super().__init__(config)
        self.power_rating = config['modules']['heat_pump']['power_rating']  # kW
        self.input_temperature = None