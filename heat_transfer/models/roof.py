from ..generic import *
from object_layer import *
class Roof(MultiLayerObject, SurfaceAreaObject):
    def __init__(self, layers, length, width, temperature_1, temperature_2):
        MultiLayerObject.__init__(self, layers, temperature_1, temperature_2)
        self.length = length
        self.width = width

    
    def get_surface_area(self):
        return self.length * self.width