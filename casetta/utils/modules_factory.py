from casetta.modules.energy_exchange_manager import EnergyExchangeManager
from casetta.modules.base_module import EnergyProducer, EnergyConsumer
from casetta.modules.building import Building
from casetta.modules.electric_battery import ElectricBattery
from casetta.modules.grid import Grid
from casetta.modules.hvac import Hvac
from casetta.modules.photovoltaic import PhotovoltaicPanel


def create_modules(config):
    modules = {}
    energy_producers = {}
    energy_consumers = {}

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
        else:
            raise ValueError(f"Unknown module type: {name}")

        if isinstance(modules[name], EnergyProducer):
            energy_producers[name] = modules[name]

        if isinstance(modules[name], EnergyConsumer):
            energy_consumers[name] = modules[name]

    modules['energy_exchange'] = EnergyExchangeManager(
        energy_producers=energy_producers,
        energy_consumers=energy_consumers,
        config={}
    )


    return modules['energy_exchange']