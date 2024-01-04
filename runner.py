from heat_transfer.conduction import *
from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.generic import *



room1 = Room((5, 5, 3), 
             20)

room2 = Room((5, 5, 3),
            20)

house = House([room1, room2],
              interfaces=[[[room1, room2], 0]],
              wall_layers=[(0.03, Material(2000, 500, 0.03)), (0.07, Material(1500, 800, 0.02))],
              roof_layers=[(0.1, Material(1225, 1005, 0.024))],
              floor_layers=[(0.1, Material(1225, 1005, 0.024))])