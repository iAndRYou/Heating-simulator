from ..generic import *
from ..model_parameters import Config
from .room import *


class RadiatorHeating(HeatingSystem):
    max_heat_power: float # W
    heat_power: dict[HeatingUnit, float] # W
    new_heat_power: dict[HeatingUnit, float] # W

    def __init__(self, units: dict[Room, int], max_heat_power: float = 2000):
        self.max_heat_power = max_heat_power
        self.heat_power = {HeatingUnit(room, i): 0 for room in units.keys() for i in range(units[room])}
        self.update_heat_power(0)

    
    def update_heat_power(self, time_passed: float):
        for unit in list(self.heat_power.keys()):
            room = unit.room
            if room.temperature < Config().TARGET_TEMPERATURE:
                self.heat_power[unit] = 1000
            else:
                self.heat_power[unit] = 0
        super().update_heat_power(time_passed)

    def heat_flow(self) -> dict["UniformTemperatureObject", float]:
        object_heat: dict[UniformTemperatureObject, float] = dict()

        for unit, heat_power in list(self.heat_power.items()):
            room = unit.room
            heat = heat_power * Config().TIME_STEP
            if room in object_heat:
                object_heat[room] += heat
            else:
                object_heat[room] = heat
            self.spent_energy += heat
        
        return object_heat

        

class GasFurnaceHeating(HeatingSystem):
    max_heat_power: float # W
    heat_power: dict[HeatingUnit, float] # W
    new_heat_power: dict[HeatingUnit, float] # W

    current_heat_power: float

    def __init__(self, rooms: list[Room], max_heat_power: float = 40000):
        self.max_heat_power = max_heat_power
        self.heat_power = {HeatingUnit(room, 0): 0 for room in rooms}
        self.current_heat_power = 0
        self.update_heat_power(0)

    def update_heat_power(self, time_passed: float):
        rooms = [unit.room for unit in self.heat_power.keys()]
        mean_temperature_gap = sum(room.temperature - Config().TARGET_TEMPERATURE for room in rooms) / len(rooms)

        if mean_temperature_gap < 0: 
            if self.current_heat_power < self.max_heat_power:
                self.current_heat_power += 30 * (time_passed - self.last_power_update_time)/60
        else:
            if self.current_heat_power > 0:
                self.current_heat_power -= 30 * (time_passed - self.last_power_update_time)/60
            
        for unit in list(self.heat_power.keys()):
            self.heat_power[unit] = self.current_heat_power / len(self.heat_power)

        super().update_heat_power(time_passed)

    def heat_flow(self) -> dict["UniformTemperatureObject", float]:
        object_heat: dict[UniformTemperatureObject, float] = dict()
        for unit, heat_power in self.heat_power.items():
            room = unit.room
            heat = heat_power * Config().TIME_STEP
            if room in object_heat:
                object_heat[room] += heat
            else:
                object_heat[room] = heat
            self.spent_energy += heat
        
        return object_heat



class HeatPumpHeating(HeatingSystem):
    max_heat_power: float # W
    heat_power: dict[HeatingUnit, float] # W
    new_heat_power: dict[HeatingUnit, float] # W

    current_heat_power: float

    def __init__(self, rooms: list[Room], max_heat_power: float = 25000):
        self.max_heat_power = max_heat_power
        self.heat_power = {HeatingUnit(room, 0): 0 for room in rooms}
        self.current_heat_power = 0
        self.update_heat_power(0)

    def update_heat_power(self, time_passed: float):
        rooms = [unit.room for unit in self.heat_power.keys()]
        mean_temperature_gap = sum(room.temperature - Config().TARGET_TEMPERATURE for room in rooms) / len(rooms)

        if mean_temperature_gap < 0: 
            if self.current_heat_power < self.max_heat_power:
                self.current_heat_power += 10 * (time_passed - self.last_power_update_time)/60
        else:
            if self.current_heat_power > -self.max_heat_power:
                self.current_heat_power -= 10 * (time_passed - self.last_power_update_time)/60
            
        for unit in list(self.heat_power.keys()):
            self.heat_power[unit] = self.current_heat_power / len(self.heat_power)

        super().update_heat_power(time_passed)

    def heat_flow(self) -> dict["UniformTemperatureObject", float]:
        object_heat: dict[UniformTemperatureObject, float] = dict()
        for unit, heat_power in self.heat_power.items():
            room = unit.room
            heat = heat_power * Config().TIME_STEP
            if room in object_heat:
                object_heat[room] += heat
            else:
                object_heat[room] = heat
            self.spent_energy += heat
        
        return object_heat
