from typing import List, Dict, Tuple, Any
from .object_layer import *
from ..generic import *

class Wall(MultiLayerObject):
    def __init__(self, layers, length, height, temperature_1, temperature_2, openings = []):
        MultiLayerObject.__init__(self, layers, temperature_1, temperature_2)
        self.length = length
        self.height = height
        self.openings : List[Opening] = openings

    
    
    def get_surface_area(self):
        return self.length * self.height - sum(opening.get_surface_area() for opening in self.openings)
    
   
         

    