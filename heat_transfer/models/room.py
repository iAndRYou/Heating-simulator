from .heating_systems import *
from ..generic import *


AIR = Material(1225, 1005, 0.024)
ENVIRONMENT = UniformTemperatureObject(20, Material(1225, 1005, 0.024))
GROUND = UniformTemperatureObject(10, Material(1225, 1005, 0.024))

class Room(UniformTemperatureObject):
    dimensions: tuple[float, float, float]
    walls: list[MultiLayerObject]
    roof: MultiLayerObject
    floor: MultiLayerObject

    def __init__(self, dimensions, init_temperature_celsius):
        super().__init__(init_temperature_celsius, AIR, prod(dimensions))

        self.dimensions = dimensions
        self.walls = []
        self.roof = None
        self.floor = None
