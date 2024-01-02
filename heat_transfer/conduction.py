from typing import List, Dict, Tuple, Any
from .models.wall import *


class Conduction:
    def __init__(self, time_step : float):
        self.time_step = time_step
        
    def update_temperature(self, wall : Wall):
        total_resistance = sum(layer.thickness / layer.conductivity for layer in wall.layers)
        heat_flux_density = (wall.temperature_1 - wall.temperature_2) / total_resistance

        layer1, layer2 = wall.layers[0], wall.layers[-1]
        delta_temperature_1 = heat_flux_density * self.time_step / (layer1.specific_heat_capacity * layer1.density * layer1.thickness)
        delta_temperature_2 = heat_flux_density * self.time_step / (layer2.specific_heat_capacity * layer2.density * layer2.thickness)
        # wall.temperature_1 -= delta_temperature_1
        # wall.temperature_2 += delta_temperature_2
        return delta_temperature_1, delta_temperature_2
