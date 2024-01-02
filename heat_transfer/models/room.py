from .wall import *
from .roof import *
from .floor import *
from .heating_systems import *
from ..generic import *


class Room:

    def __init__(self, walls, roof, floor, temperature, heating_systems = [], name = "Room"):
        self.__arg_requriements(walls, roof, floor)
        
        self.walls : List[Wall] = walls
        self.roof : Roof = roof
        self.floor : Floor = floor
        self.temperature : float = temperature
        self.heating_systems : List[HeatingSystem] = heating_systems
        self.name : str = name

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
        if not ((walls[0].length == walls[2].length and walls[1].length == walls[3].length) or
                (walls[0].length == walls[1].length and walls[2].length == walls[3].length)):
            raise ValueError("Two pairs of opposite walls must have the same length.")
        if roof.length != floor.length or roof.width != floor.width:
            raise ValueError("The roof and floor must have the same dimensions.")
        if roof.length != walls[0].length or roof.width != walls[1].length:
            raise ValueError("The roof and walls must have matching dimensions.")
    
    