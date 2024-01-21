from .generic import UniformTemperatureObject, Material


TIME_STEP = 1 # s
NODE_DISTANCE = 0.03 # m
AIR = Material(1225, 1005, 0.024)
GLASS = Material(2500, 840, 1)
WOOD = Material(300, 1800, 0.1)
ENVIRONMENT = UniformTemperatureObject(15, Material(1225, 1005, 0.024), object_type="environment")
GROUND = UniformTemperatureObject(15, Material(1500, 1200, 1), object_type="ground")


class Config:
    TIME_STEP: float
    NODE_DISTANCE: float
    AIR: Material
    GLASS: Material
    WOOD: Material
    ENVIRONMENT: UniformTemperatureObject
    GROUND: UniformTemperatureObject

    _shared_state = dict()

    def __init__(self):
        self.__dict__ = self._shared_state

    def __getitem__(self, key):
        return self._shared_state[key]

    def __setitem__(self, key, value):
        self._shared_state[key] = value

Config().TIME_STEP = TIME_STEP
Config().NODE_DISTANCE = NODE_DISTANCE
Config().AIR = AIR
Config().GLASS = GLASS
Config().WOOD = WOOD
Config().ENVIRONMENT = ENVIRONMENT
Config().GROUND = GROUND
