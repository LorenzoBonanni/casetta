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

    def to_numpy(self):
        return np.array(
            [
                self.non_shiftable_load,
                self.internal_temperature,
                self.external_temperature,
                self.ground_temperature,
                self.solar_irradiation,
                self.thermal_set_point,
                self.weekday,
                self.day,
                self.month,
                self.year,
                self.hour,
                self.minute,
                self.domestic_hot_water_request
            ]
        )

    def __copy__(self):
        return deepcopy(self)