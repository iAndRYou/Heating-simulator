from heat_transfer.conduction import *
from heat_transfer.models.wall import *
from heat_transfer.models.object_layer import *


wall = Wall([ObjectLayer(0.05, 0.026, 780, 500), ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 100)
conduction = Conduction(1)
conduction.update_temperature(wall)


# for i in range(10000):
#     conduction.update_temperature(wall)

print(wall.temperature_1)
print(wall.temperature_2)



