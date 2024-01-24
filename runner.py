from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.generic import *
from heat_transfer.model_parameters import Config
from heat_transfer.models.heating_systems import *
from heat_transfer.visualization import *
from matplotlib import pyplot as plt
import numpy as np
from vpython import *
from heat_transfer.temperature_plot import Plot

def get_environment_temperature_step(hours_passed):
    days = hours_passed // 24
    hours = hours_passed % 24


    if hours < 12:
        previous_peak = 15 + 7/5*days
        next_peak = 24 + 14/5*days
    else:
        previous_peak = 24 + 14/5*days
        next_peak = 15 + 7/5*(days+1)

    return (next_peak - previous_peak) * (hours%12) / 12 + previous_peak

def get_environment_temperature_sin(hours_passed):
    days = hours_passed // 24
    hours = hours_passed % 24

    return 10 + 12/5*days + 6*np.sin(2*np.pi*hours/24)

def get_environment_temperature_increase(hours_passed):
    if hours_passed < 72:
        return 15
    else:
        return 30

def get_environment_temperature_decrease(hours_passed):
    if hours_passed < 72:
        return 15
    else:
        return -5


room1 = Room(1,
             (4, 3, 4), 
             10,
             vector(5, 0, 0),
             parent=None)

room2 = Room(2,
            (6, 3, 4),
            10,
            vector(0, 0, 0),
            parent=None)

room3 = Room(3,
            (6, 3, 3),
            10,
            vector(0, 0, 3.5),
            parent=None)

# heating_system = RadiatorHeating(units={room1: 2, room2: 4, room3: 2})
# heating_system = GasFurnaceHeating(rooms=[room1, room2, room3])
heating_system = HeatPumpHeating(rooms=[room1, room2, room3])

house = House([room1, room2, room3],
              interfaces=[[[room2, room1], Direction(Axis.X, True)], [[room2, room3], Direction(Axis.Z, True)]],
              wall_layers=[(0.1, Config().CONCRETE)],
              roof_layers=[(0.1, Config().CONCRETE)],
              floor_layers=[(0.1, Config().CONCRETE)],
              heating_system=heating_system,
              local_position=vector(0, 0, 0))


room1.add_windows(Direction(Axis.Z, False), 1)
room1.add_windows(Direction(Axis.Z, True), 1)
room1.add_windows(Direction(Axis.X, True), 1)
room1.add_door(Direction(Axis.X, False))

room2.add_door(Direction(Axis.Z, True))
room2.add_windows(Direction(Axis.Z, False), 2)
room2.add_windows(Direction(Axis.X, False), 1)

room3.add_windows(Direction(Axis.Z, True), 2)
room3.add_windows(Direction(Axis.X, True), 1)
room3.add_windows(Direction(Axis.X, False), 1)

scene = Scene(house.print_rooms_temperatures)

house.setup_visuals()


UPDATE_STEP = 3 # in hours
TIME_LIMIT = 144 # in hours


plot = Plot(rooms=[room1, room2, room3], max_hours=TIME_LIMIT)

hours_passed = 0
for i in range(TIME_LIMIT // UPDATE_STEP):
    Config().ENVIRONMENT.temperature = get_environment_temperature_increase(hours_passed) + 273.15
    Config().GROUND.temperature = get_environment_temperature_increase(hours_passed) + 273.15
    scene.update_slider_values()
    for j in range(UPDATE_STEP * 3600 // Config().TIME_STEP):
        house.update_temperature()
        scene.update_scene()
        heating_system.update_heat_power(hours_passed*3600 + j*Config().TIME_STEP)
    hours_passed = UPDATE_STEP*(i+1)

    house.update_visuals()
    scene.update_text(hours_passed)
    plot.update(hours_passed)
    print(f"{hours_passed} hours passed")

plt.show()
input()
