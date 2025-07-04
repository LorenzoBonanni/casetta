from casetta.modules.core.base_exchange_manager import BaseExchangeManager


class ThermalExchangeManager(BaseExchangeManager):
    def consume_callback(self, consumer, produced):
        consumer.consume_thermal_energy(produced)

    def produce_callback(self, producer, value):
        return producer.produce_thermal_energy(value)

    def __init__(self, thermal_producers, thermal_consumers):
        super().__init__(
            producers=thermal_producers,
            consumers=thermal_consumers,
            prefix="thermal"
        )
