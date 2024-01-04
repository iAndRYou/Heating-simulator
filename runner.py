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


wall1 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)
wall2 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)
wall3 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)
wall4 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)

roof = Roof([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
floor = Floor([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)


roof2 = Roof([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
floor2 = Floor([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)


"""
room1 = Room([wall1, wall2, wall3, wall4], roof, floor, -30, [], "Room", pos=vector(-1, 0, 0))
room1.make_room_model()
room = Room([wall1, wall2, wall3, wall4], roof, floor, -20, [], "Room", pos=vector(0, 0, 0))
room.make_room_model()
room2 = Room([wall1, wall2, wall3, wall4], roof2, floor2, -10,  [], "Room2", pos=vector(1, 0, 0))
room2.make_room_model()
room3 = Room([wall1, wall2, wall3, wall4], roof2, floor2, 0,  [], "Room2", pos=vector(2, 0, 0))
room3.make_room_model()
room4 = Room([wall1, wall2, wall3, wall4], roof2, floor2, 10,  [], "Room2", pos=vector(3, 0, 0))
room4.make_room_model()
room5 = Room([wall1, wall2, wall3, wall4], roof2, floor2, 20,  [], "Room2", pos=vector(4, 0, 0))
room5.make_room_model()
room6 = Room([wall1, wall2, wall3, wall4], roof2, floor2, 30,  [], "Room2", pos=vector(5, 0, 0))
room6.make_room_model()
room7 = Room([wall1, wall2, wall3, wall4], roof2, floor2, 40,  [], "Room2", pos=vector(7, 0, 0))
room7.make_room_model()

"""