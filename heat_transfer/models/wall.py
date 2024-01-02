from typing import List, Dict, Tuple, Any
from .object_layer import *
from ..generic import *

class Wall(MultiLayerObject):
    def __init__(self, layers, length, height, temperature_1, temperature_2):
        MultiLayerObject.__init__(self, layers, temperature_1, temperature_2)
        length = length
        height = height

    @property
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)
    
   
         

    