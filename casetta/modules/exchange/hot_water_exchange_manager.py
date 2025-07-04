from casetta.modules.core.base_exchange_manager import BaseExchangeManager


class HotWaterExchangeManager(BaseExchangeManager):
    def consume_callback(self, consumer, produced):
        consumer.consume_hot_water(produced)

    def produce_callback(self, producer, value):
        return producer.produce_hot_water(value)

    def __init__(self, hot_water_producers, hot_water_consumers):
        super().__init__(
            producers=hot_water_producers,
            consumers=hot_water_consumers,
            prefix="hot_water"
        )
