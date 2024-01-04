from .room import Room
from ..generic import *

class House(Model3D):
    def __init__(self, rooms, pos):
        Model3D.__init__(self, Model3DParams(local_pos=pos, size=vector(0, 0, 0)))
        self.rooms : List[Room] = rooms
        
    def init(self):
        for room in self.rooms:
            room.set_parent(self)
            room.make_room_model()
        
    