from .room import Room

class House:
    def __init__(self, rooms):
        self.rooms : List[Room] = rooms
        
    