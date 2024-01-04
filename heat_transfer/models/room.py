from .wall import *
from .roof import *
from .floor import *
from .heating_systems import *
from ..generic import *


class Room(Model3D):

    def __init__(self, walls, roof, floor, temperature, heating_systems = [], name = "Room", pos = vector(0, 0, 0)):
        self.__arg_requriements(walls, roof, floor)
        
        self.walls : List[Wall] = walls
        self.roof : Roof = roof
        self.floor : Floor = floor
        self.temperature : float = temperature
        self.heating_systems : List[HeatingSystem] = heating_systems
        self.name : str = name
        self.pos = pos
        
        Model3D.__init__(self, Model3DParams(local_pos=self.pos, size=vector(self.length, self.height, self.width)))

    @property
    def length(self):
        return self.walls[0].length
    @property
    def width(self):
        return self.walls[1].length
    @property
    def height(self):
        return self.walls[0].height
    
    def volume(self):
        return self.length * self.width * self.height


    def __str__(self):
        return f'{self.name} ({self.length} x {self.width} x {self.height})'
    
    def __arg_requriements(self, walls, roof, floor):
        if not (isinstance(walls, list) and all(isinstance(wall, Wall) for wall in walls)) or len(walls) != 4:
            raise ValueError("The list of walls must be a list of 4 walls")
        if not all(wall.height == walls[0].height for wall in walls):
            raise ValueError("All walls must have the same height.")
        if not (walls[0].length == walls[2].length and walls[1].length == walls[3].length):
            raise ValueError("Two pairs of opposite walls must have the same length.")
        if roof.length != floor.length or roof.width != floor.width:
            raise ValueError("The roof and floor must have the same dimensions.")
        if roof.length != walls[0].length or roof.width != walls[1].length:
            raise ValueError("The roof and walls must have matching dimensions.")
    
    def make_room_model(self):
        self.make_box()
        self.shape.opacity = 0.85
        self.shape.color = color.red
        for i in range(len(self.walls)):
            if(self.walls[i].parent != None):
                continue
            rot = (0, vector(0, 0, 1))
            if(i % 2 == 0):
                z = self.walls[1].length/2
                z = z if i < 2 else z * (-1)
                local_pos = vector(0, 0, z)
            else:
                x = self.walls[0].length/2
                x = x if i < 2 else x * (-1)
                local_pos = vector(x, 0, 0)
                rot=(pi/2, vector(0, 1, 0))
            self.walls[i].local_pos = local_pos
            self.walls[i].rot = rot
            self.walls[i].set_parent(self)
            self.walls[i].make_box()
            
        