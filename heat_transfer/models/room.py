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
        self.shape.opacity = 0.7
        self.shape.color = self.map_temperature_to_color(self.temperature)
        self.add_openings()
        
    
    def add_openings(self):
        for i in range(len(self.walls)):
            wall = self.walls[i]
            if i % 2 == 0:
                z_offset = self.width / 2
                z_offset *= -1 if i == 0 else 1
                
                openings = wall.openings
                num_openings = len(openings)
                distance_between_windows = wall.length / (num_openings + 1)
                initial_position = distance_between_windows - wall.length / 2

                print(f"num_openings: {num_openings}, distance_between_windows: {distance_between_windows}, initial_position: {initial_position}")
                for j in range(num_openings):
                    opening = openings[j]
                    if hasattr(opening, "parent"):
                        continue
                    opening_x_position = initial_position + j * distance_between_windows
                    opening.initModel3D(Model3DParams(local_pos=vector(opening_x_position, 0, z_offset), size=vector(opening.length, opening.height, 0.1), parent=self))
                    opening.make_box()
            else:
                x_offset = self.length / 2
                x_offset *= -1 if i == 1 else 1
                
                openings = wall.openings
                num_openings = len(openings)
                distance_between_windows = wall.length / (num_openings + 1)
                initial_position = distance_between_windows - wall.length / 2

                for j in range(num_openings):
                    opening = openings[j]
                    if hasattr(opening, "parent"):
                        continue
                    opening_z_position = initial_position + j * distance_between_windows
                    opening.initModel3D(Model3DParams(local_pos=vector(x_offset, 0, opening_z_position), size=vector(opening.length, opening.height, 0.1), rot=(pi/2, vector(0, 1, 0)), parent=self))
                    opening.make_box()
                    
                    
            
        
       
    
    def update_color(self):
        self.shape.color = self.map_temperature_to_color(self.temperature)
        
    def on_temperature_change(self, delta_temperature):
        self.temperature += delta_temperature
        self.update_color()
            
        