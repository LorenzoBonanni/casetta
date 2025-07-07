from casetta_env.modules.core.base_exchange_manager import BaseExchangeManager


class EnergyExchangeManager(BaseExchangeManager):
    def consume_callback(self, consumer, produced):
        consumer.consume_electric_energy(produced)

    def produce_callback(self, producer, value):
        return producer.produce_electric_energy(value)

    def __init__(self, energy_producers, energy_consumers):
        super().__init__(
            producers=energy_producers,
            consumers=energy_consumers,
            prefix="energy"
        )
