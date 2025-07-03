from dataclasses import dataclass

@dataclass
class BuildingOutput:
    non_shiftable_load: float
    internal_temperature: float
    external_temperature: float
    ground_temperature: float
    solar_irradiation: float
    thermal_set_point: float
    weekday: int
    day: int
    month: int
    year: int
    hour: int
    minute: int
    domestic_hot_water_request: float
    unmet_energy_load: float
    consumed_energy: float

@dataclass
class GridOutput:
    buy_price: float
    sell_price: float
    sold_energy: float
    bought_energy: float

@dataclass
class ElectricBatteryOutput:
    soc: float
    stored_energy: float
    charged_energy: float
    discharged_energy: float

@dataclass
class PhotovoltaicOutput:
    energy_produced: float

@dataclass
class HvacOutput:
    consumed_electric_energy: float
    consumed_thermal_energy: float
    delta_temperature: float

@dataclass
class HeatPumpOutput:
    consumed_electric_energy: float
    produced_thermal_energy: float