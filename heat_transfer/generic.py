from vpython import *
from dataclasses import dataclass
from typing import List, Tuple, Any

class MultiLayerObject:
    def __init__(self, layers, temperature_1, temperature_2):
        self.layers : List[ObjectLayer] = layers  
        self.temperature_1 : float = temperature_1  
        self.temperature_2 : float = temperature_2
        
    @property   
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)

    def get_surface_area(self):
        return 0
    

class Opening(MultiLayerObject):
    def get_surface_area(self):
        return 0
    
class HeatingSystem:
    def __init__(self, name, power, temperature):
        self.name = name
        self.power = power
        self.temperature = temperature
        
        
@dataclass
class Model3DParams:
    local_pos: vector 
    size: vector 
    rot: Tuple[float, vector] = (0, vector(0, 0, 1)) #rot = (angle, axis : vector())
    parent: 'Model3D' = None
    shape: Any = None
        
class Model3D:
    def __init__(self, params : Model3DParams):
        self.local_pos = params.local_pos
        self.size = params.size
        self.rot = params.rot
        self.parent = params.parent
        self.shape = params.shape
        self.update_position()
        
    def set_parent(self, parent):
        self.parent = parent
        self.update_position()
        
    def update_position(self):
        if self.parent:
            self.pos = self.parent.pos + self.local_pos
        else:
            self.pos = self.local_pos
            
    def make_box(self):
        self.update_position()
        self.shape = box(pos=self.pos, size=self.size, opacity=0.85)
        self.shape.rotate(angle=self.rot[0], axis=self.rot[1])
    
    

    
