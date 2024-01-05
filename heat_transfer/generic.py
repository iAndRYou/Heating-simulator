from math import prod
from .model_parameters import Config
from enum import Enum

# from .models.object_layer import ObjectLayer

class ObjectLayer:
    thickness: float
    material: "Material"
    parent_object: "MultiLayerObject"
    nodes: list["UniformTemperatureObject"]

    def __init__(self, init_temperature_celsius: float, thickness: float, material: "Material", parent_object: "MultiLayerObject"):
        self.thickness = thickness
        self.material = material
        self.parent_object = parent_object

        self.nodes = [UniformTemperatureObject(init_temperature_celsius, material, self.parent_object.area*Config().NODE_DISTANCE) for _ in range(int(thickness // Config().NODE_DISTANCE))]


class MultiLayerObject:
    layers: list[ObjectLayer]
    height: float
    width: float
    border: list["UniformTemperatureObject"]

    def __init__(self, height, width, init_temperature_celsius: float, layers: list[list[float, "Material"]], border: list["UniformTemperatureObject"], openings: dict[tuple[float, float], "MultiLayerObject"] = dict()):
        self.height = height
        self.width = width
        self.layers: list[ObjectLayer] = [ObjectLayer(init_temperature_celsius, thickness, material, self) for thickness, material in layers]
        self.openings = openings
        self.border = border
        
    @property   
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)
    
    @property
    def area(self):
        return self.height * self.width

    @property
    def nodes(self):
        return [node for layer in self.layers for node in layer.nodes]

    
class HeatingSystem:
    def __init__(self, name, power, temperature):
        self.name = name
        self.power = power
        self.temperature = temperature
    


class Material:
    density: float # kg/m^3
    specific_heat_capacity: float # J/(kg*K)
    conductivity: float # W/(m*K)

    def __init__(self, density: float, specific_heat_capacity: float, conductivity: float):
        self.density = density
        self.specific_heat_capacity = specific_heat_capacity
        self.conductivity = conductivity


class UniformTemperatureObject:
    temperature: float # K
    material: Material
    volume: float | None = None # m^3

    def __init__(self, temperature_celsius: float, material: Material, volume: float | None = None):
        self.temperature = temperature_celsius + 273.15
        self.material = material
        self.volume = volume

    @property
    def mass(self) -> float:
        return self.volume * self.material.density

    def update_temperature(self, heat: int):
        if self.volume is not None:
            self.temperature += heat / (self.material.specific_heat_capacity * self.mass)

        # else:  infinite heat capacity -> temperature does not change
