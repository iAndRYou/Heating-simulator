from .heating_systems import *
from ..generic import *


AIR = Material(1225, 1005, 0.024)
ENVIRONMENT = UniformTemperatureObject(0, Material(1225, 1005, 0.024))
GROUND = UniformTemperatureObject(0, Material(1225, 1005, 0.024))

class Room(UniformTemperatureObject, Object3D):
    dimensions: tuple[float, float, float]
    walls: list[MultiLayerObject]
    roof: MultiLayerObject
    floor: MultiLayerObject

    def __init__(self, dimensions, init_temperature_celsius,
                 local_position = vector(0, 0, 0), parent: "Object3D" = None):
        super().__init__(init_temperature_celsius, AIR, prod(dimensions))

        self.dimensions = dimensions
        self.walls = []
        self.roof = None
        self.floor = None
        Object3D.__init__(self, dimensions=tuple_to_vector(dimensions), local_position=local_position, parent=parent)
    
    def on_temperature_change(self):
        if self.shape:
            self.shape.color = self.map_temperature_to_color(self.temperature)
