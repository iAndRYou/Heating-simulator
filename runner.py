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
from heat_transfer.generic import *
from vpython import *
from dataclasses import dataclass


wall1 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(1, 1, 0)))
wall2 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(2, 1, 0)))
wall3 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(1, 1, 0)))
wall4 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(2, 1, 0)))
wall5 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(2, 1, 0)))
wall6 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(2, 1, 0)))
wall7 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(2, 1, 0)))
wall8 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, [], Model3DParams(local_pos=vector(0, 0, 0), size=vector(2, 1, 0)))

roof = Roof([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)
floor = Floor([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)


roof2 = Roof([ObjectLayer(0.1, 0.026, 780, 500)], 2, 2, 20, 20)
floor2 = Floor([ObjectLayer(0.1, 0.026, 780, 500)], 2, 2, 20, 20)
room2 = Room([wall8, wall5, wall6, wall7], roof2, floor2, [], "Room2", pos=vector(2, 0, 0))
room2.make_room_model()
room = Room([wall1, wall2, wall3, wall4], roof, floor, [], "Room", pos=vector(0, 0, 0))
room.make_room_model()
