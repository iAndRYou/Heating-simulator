from heat_transfer.conduction import *
from heat_transfer.models.wall import *
from heat_transfer.models.roof import *
from heat_transfer.models.floor import *
from heat_transfer.models.window import *
from heat_transfer.models.door import *
from heat_transfer.models.object_layer import *
from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.models.heating_systems import *


wall = Wall([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100)
wall2 = Wall([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 2, 1, 20, 100)
conduction = Conduction(1)
conduction.update_temperature(wall)


# for i in range(10000):
#     conduction.update_temperature(wall)

print(wall.temperature_1)
print(wall.temperature_2)
print(wall.get_surface_area())
r =Roof([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 100)
f = Floor([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 100)
w = Window([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100)
d = Door([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100)


room = Room([wall, wall2, wall, wall2], r, f, 20)

hs = Radiator(1000, 30)
room.heating_systems.append(hs)
print(room.volume())
house = House([room])