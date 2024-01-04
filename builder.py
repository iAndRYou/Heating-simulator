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

def build():
    # windows and doors
    window = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window2 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window3 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window4 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window5 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window6 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window7 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window8 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    window9 = Window([ObjectLayer(0.1, 0.026, 780, 500)], 1, 1, 20, 20)
    door2 = Door([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)
    door3 = Door([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)
    door = Door([ObjectLayer(0.1, 0.026, 780, 500)], 1, 2, 20, 20)


    # walls, roof, floor
    # wall4 shared between room1 and room2
    
    wall1 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 10, 4, 20, 20, [window, door])
    wall2 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 4, 20, 20, [window2, window3, window4])
    wall3 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 10, 4, 20, 20, [window5, window6, window7, window8, window9])
    wall4 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 4, 20, 20, [door2])
    
    wall5 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 4, 20, 20, [door3])
    wall6 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 4, 20, 20)
    wall7 = Wall([ObjectLayer(0.1, 0.026, 780, 500)], 20, 4, 20, 20)

    roof = Roof([ObjectLayer(0.1, 0.026, 780, 500)], 10, 20, 20, 20)
    floor = Floor([ObjectLayer(0.1, 0.026, 780, 500)], 10, 20, 20, 20)

    roof2 = Roof([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, 20, 20)
    floor2 = Floor([ObjectLayer(0.1, 0.026, 780, 500)], 20, 20, 20, 20)

    room1 = Room([wall1, wall2, wall3, wall4], roof, floor, 10, [], "Room", pos=vector(0, 0, 0))
    room1.make_room_model()

    room2 = Room([wall5, wall4, wall6, wall7], roof2, floor2, 26,  [], "Room2", pos=vector(15.01, 0, 0))
    room2.make_room_model()

    """

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