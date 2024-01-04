from vpython import *
from dataclasses import dataclass
from typing import List, Tuple, Any
from colorsys import hsv_to_rgb

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
        if self.shape:
            self.shape.pos = self.pos
            
    def make_box(self):
        self.update_position()
        self.shape = box(pos=self.pos, size=self.size, opacity=0.8)
        if(self.rot[0] != 0 or self.rot[1] != vector(0, 0, 1)):
            self.shape.rotate(angle=self.rot[0], axis=self.rot[1])
        
    def map_temperature_to_color(self, temperature):
        normalized_temperature = (temperature + 50) / 100 # temp scale from -50 to 50
        h = 1 * (1 - normalized_temperature)  # H 
        s = 0.8  # Saturation
        v = 1.0  # Value
        
        color_rgb = hsv_to_rgb(h, s, v)
        return vector(color_rgb[0], color_rgb[1], color_rgb[2])
    
    def rotate(self, angle, axis):
        if self.shape:
            self.shape.rotate(angle=angle, axis=axis)
        
    def change_pos(self, pos):
        self.local_pos = pos
        self.update_position()

class Opening(MultiLayerObject, Model3D):
    def get_surface_area(self):
        return 0
    
    def initModel3D(self, params):
        Model3D.__init__(self, params)
    
class HeatingSystem:
    def __init__(self, name, power, temperature):
        self.name = name
        self.power = power
        self.temperature = temperature
        
        


       
    
    

    
