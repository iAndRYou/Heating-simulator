from ..generic import *
from ..model_parameters import Config
from .room import *


class RadiatorHeating(HeatingSystem):
    heat_power: float = 1000 # W

    def __init__(self, rooms: list[Room]):
        self.rooms = rooms

    def heat_flow(self) -> dict[UniformTemperatureObject, float]:
        object_heat: dict[UniformTemperatureObject, float] = dict()
        for room in self.rooms:
            if room.temperature < Config().TARGET_TEMPERATURE:
                object_heat[room] = self.heat_power * Config().TIME_STEP
        
        return object_heat
