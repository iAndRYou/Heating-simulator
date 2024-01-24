from math import prod
from enum import Enum, IntEnum
from dataclasses import dataclass

from vpython import vector

class Axis(IntEnum):
    X = 0
    Y = 1
    Z = 2


@dataclass(frozen=True)
class Direction:
    axis: Axis
    positive: bool

class HeatingUnit:
    room: "Room"
    ind: int

    def __init__(self, room: "Room", ind: int):
        self.room = room
        self.ind = ind
    
class HeatingSystem:
    heat_power: dict[HeatingUnit, float] # W
    new_heat_power: dict[HeatingUnit, float] # W
    last_power_update_time: float = 0 # seconds

    spent_energy: float = 0 # J

    def update_heat_power(self, time_passed: float) -> None:
        self.last_power_update_time = time_passed

    def heat_flow(self) -> dict["UniformTemperatureObject", float]:
        raise NotImplementedError


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
    object_type: str | None

    def __init__(self, temperature_celsius: float, material: Material, volume: float | None = None, object_type: str | None = None):
        self.temperature = temperature_celsius + 273.15
        self.material = material
        self.volume = volume
        self.object_type = object_type

    @property
    def mass(self) -> float:
        return self.volume * self.material.density

    def update_temperature(self, heat: int):
        if self.volume is not None:
            self.temperature += heat / (self.material.specific_heat_capacity * self.mass)

        # else:  infinite heat capacity -> temperature does not change

    def __str__(self):
        return f"{self.object_type} at {self.temperature} K"

    def __repr__(self):
        return f"{self.object_type} at {self.temperature} K"
