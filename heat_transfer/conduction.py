from typing import List, Dict, Tuple, Any

class Conduction:
    def __init__(self, time_step : float):
        self.time_step = time_step
        
    def update_temperature(self, wall : Wall):
        total_conductance = sum(layer.thickness / layer.conductivity for layer in wall.layers)
        heat_flux_density = -(wall.temperature_1 - wall.temperature_2) / total_conductance
        delta_temperature = heat_flux_density * self.time_step / wall.get_total_rho_cp()
        wall.temperature_1 += delta_temperature
        wall.temperature_2 -= delta_temperature
