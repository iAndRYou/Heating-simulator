from math import prod
from enum import Enum

from vpython import vector
from .visualization import *


    
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

