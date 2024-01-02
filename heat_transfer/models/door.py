from ..generic import *
class Door(Opening):
    def __init__(self, layers, length, height, temperature_1, temperature_2):
        MultiLayerObject.__init__(self, layers, temperature_1, temperature_2)
        self.length = length
        self.height = height
    def get_surface_area(self):
        return self.length * self.height