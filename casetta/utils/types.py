from copy import deepcopy
from dataclasses import dataclass

import numpy as np


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
    battery2house_energy: float
    battery2grid_energy: float
    grid2battery_energy: float