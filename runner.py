from heat_transfer.conduction import *
from heat_transfer.models.wall import *
from heat_transfer.models.roof import *
from heat_transfer.models.floor import *
from heat_transfer.models.window import *
from heat_transfer.models.door import *
from heat_transfer.models.object_layer import *


wall = Wall([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100)
conduction = Conduction(1)
conduction.update_temperature(wall)


# for i in range(10000):
#     conduction.update_temperature(wall)

print(wall.temperature_1)
print(wall.temperature_2)
print(wall.get_surface_area())
r =Roof([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100).get_surface_area()
f = Floor([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100).get_surface_area()
w = Window([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100).get_surface_area()
d = Door([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100).get_surface_area()



