from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.generic import *
from matplotlib import pyplot as plt



room1 = Room((3, 3, 3), 
             40)

room2 = Room((3, 3, 3),
            20)

house = House([room1, room2],
              interfaces=[[[room1, room2], 0]],
              wall_layers=[(0.03, Material(2000, 800, 1)), (0.07, Material(2500, 800, 1.4))],
              roof_layers=[(0.1, Material(1225, 1005, 0.024))],
              floor_layers=[(0.1, Material(1225, 1005, 0.024))])


house.print_rooms_temperatures()
node_temperatures1 = [node.temperature for node in house.rooms[0].walls[0].nodes]

for _ in range(10000):
    house.update_temperature()

node_temperatures2 = [node.temperature for node in house.rooms[0].walls[0].nodes]

# compare the node temperature distributions
plt.plot(range(len(node_temperatures1)), node_temperatures1)
plt.plot(range(len(node_temperatures2)), node_temperatures2)
plt.show()

print()

house.print_rooms_temperatures()
