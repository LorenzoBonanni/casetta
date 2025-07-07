from casetta_env.modules.building.building import Building
from casetta_env.modules.building.hvac import Hvac
from casetta_env.modules.core.energy_consumer import EnergyConsumer
from casetta_env.modules.core.energy_producer import EnergyProducer
from casetta_env.modules.core.hot_water_consumer import HotWaterConsumer
from casetta_env.modules.core.hot_water_producer import HotWaterProducer
from casetta_env.modules.core.thermal_consumer import ThermalConsumer
from casetta_env.modules.core.thermal_producer import ThermalProducer
from casetta_env.modules.electricity.electric_battery import ElectricBattery
from casetta_env.modules.electricity.grid import Grid
from casetta_env.modules.electricity.photovoltaic import PhotovoltaicPanel
from casetta_env.modules.exchange.energy_exchange_manager import EnergyExchangeManager
from casetta_env.modules.exchange.hot_water_exchange_manager import HotWaterExchangeManager
from casetta_env.modules.exchange.thermal_exchange_manager import ThermalExchangeManager
from casetta_env.modules.thermal.domestic_hot_water_tank import DomesticHotWaterTank
from casetta_env.modules.thermal.heat_pump import HeatPump
from casetta_env.modules.thermal.thermal_energy_storage import ThermalEnergyStorage


def create_modules(config):
    modules = {}
    energy_producers = {}
    energy_consumers = {}
    thermal_consumers = {}
    thermal_producer = {}
    hot_water_consumers = {}
    hot_water_producer = {}

    for name in config['modules']:
        if name == 'grid':
            modules[name] = Grid(config)
        elif name == 'electric_battery':
            modules[name] = ElectricBattery(config)
        elif name == 'building':
            modules[name] = Building(config)
        elif name == 'photovoltaic':
            modules[name] = PhotovoltaicPanel(config)
        elif name == 'hvac':
            modules[name] = Hvac(config)
        elif name == 'heat_pump':
            modules[name] = HeatPump(config)
        elif name == 'thermal_storage':
            modules[name] = ThermalEnergyStorage(config)
        elif name == 'dhw_tank':
            modules[name] = DomesticHotWaterTank(config)
        else:
            raise ValueError(f"Unknown module type: {name}")

        if isinstance(modules[name], EnergyProducer):
            energy_producers[name] = modules[name]

        if isinstance(modules[name], EnergyConsumer):
            energy_consumers[name] = modules[name]

        if isinstance(modules[name], ThermalProducer):
            thermal_producer[name] = modules[name]

        if isinstance(modules[name], ThermalConsumer):
            thermal_consumers[name] = modules[name]

        if isinstance(modules[name], HotWaterProducer):
            hot_water_producer[name] = modules[name]

        if isinstance(modules[name], HotWaterConsumer):
            hot_water_consumers[name] = modules[name]

    if len(thermal_producer) > 0:
        assert len(thermal_consumers) > 0, "Thermal producers require at least one thermal consumer"

    modules['energy_exchange'] = EnergyExchangeManager(
        energy_producers=energy_producers,
        energy_consumers=energy_consumers
    )
    modules['thermal_exchange'] = ThermalExchangeManager(
        thermal_producers=thermal_producer,
        thermal_consumers=thermal_consumers
    )
    modules['hot_water_exchange'] = HotWaterExchangeManager(
        hot_water_producers=hot_water_producer,
        hot_water_consumers=hot_water_consumers
    )


    return modules