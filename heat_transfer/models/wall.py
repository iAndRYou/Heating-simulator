from typing import List, Dict, Tuple, Any
from .object_layer import *

class Wall:
    def __init__(self, layers, length, height, temperature_1, temperature_2):
        self.layers : List[ObjectLayer] = layers  
        self.temperature_1 : float = temperature_1  
        self.temperature_2 : float = temperature_2
        self.length : float = length
        self.height : float = height
         

    def get_total_rho_cp(self):
        return sum(layer.thickness / (layer.conductivity * layer.density * layer.specific_heat_capacity) for layer in self.layers)
    
    def get_thickness(self):
        return sum(layer.thickness for layer in self.layers)