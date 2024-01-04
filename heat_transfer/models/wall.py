from typing import List, Dict, Tuple, Any
from .object_layer import *
from ..generic import *

class Wall(MultiLayerObject, Model3D):
    def __init__(self, layers, temperature_1, temperature_2, openings = [], m3d_params : Model3DParams = None):
        MultiLayerObject.__init__(self, layers, temperature_1, temperature_2)
        
        self.openings : List[Opening] = openings
        
        
        #physical properties
        self.length = m3d_params.size.x
        self.height = m3d_params.size.y
        m3d_params.size.z = self.thickness
        Model3D.__init__(self, m3d_params)
        

    @property
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)
    
    def get_surface_area(self):
        return self.length * self.height - sum(opening.get_surface_area() for opening in self.openings)
    
   
         

    