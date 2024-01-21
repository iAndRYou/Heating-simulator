from .room import *
from .layered_objects import MultiLayerObject
from ..generic import Material, UniformTemperatureObject, Direction, Axis
from ..heat_flow import HeatFlow
from ..model_parameters import Config

from itertools import product as cartesian_product


def reverse_direction(direction: Direction):
    # return (direction+2) if direction%2==direction else (direction-2)
    return Direction(direction.axis, not direction.positive)

class House(Object3D):
    rooms: list[Room]
    room_connections: dict[Room, list[tuple[Room, Direction]]] = dict()

    def __init__(self, rooms: list[Room], interfaces, wall_layers, roof_layers, floor_layers,
                 local_position = vector(0, 0, 0)):
        Object3D.__init__(self, dimensions=vector(0, 0, 0), local_position=local_position)
        self.rooms = rooms

        visited_interfaces = set()
        for room in self.rooms:
            room.set_parent(self) # visually group rooms together
            
            self.room_connections[room] = []
            for interface in interfaces:
                interface_rooms, direction = interface
                if room in interface_rooms and tuple(interface_rooms) not in visited_interfaces:
                    if room is interface_rooms[0]:
                        self.room_connections[room].append((interface_rooms[1], direction))
                    else:
                        self.room_connections[room].append((interface_rooms[0], reverse_direction(direction)))
                    visited_interfaces.add(tuple(interface_rooms))
                    

        for room in self.rooms:
            self.generate_walls(room, wall_layers)
            #room.walls = [MultiLayerObject(room.dimensions[2], room.dimensions[i%2], 20, wall_layers, border=([room, ENVIRONMENT] if i<2 else [ENVIRONMENT, room])) for i in range(4)]
            room.roof = MultiLayerObject(Axis.X, Axis.Z, room.dimensions[Axis.X], room.dimensions[Axis.Z], 20, roof_layers, border=[room, Config().ENVIRONMENT])
            room.floor = MultiLayerObject(Axis.X, Axis.Z, room.dimensions[Axis.X], room.dimensions[Axis.Z], 20, floor_layers, border=[Config().GROUND, room])
        
        for room in self.rooms:
            for room2, direction in self.room_connections[room]:
                room.walls[direction].border = [room, room2]
                room2.walls[reverse_direction(direction)] = room.walls[direction]

    
    def print_rooms_temperatures(self):
        print("ROOMS:")
        s = 'ROOMS:\n'
        for room in self.rooms:
            print(room.temperature - 273.15, "°C")
            s += "\tROOM "+ str(room.id) + ": "+ str(room.temperature - 273.15) + '\n'
        print("ENVIRONMENT:", Config().ENVIRONMENT.temperature - 273.15, "°C")
        s+= "ENVIRONMENT: "+ str(Config().ENVIRONMENT.temperature - 273.15) + '\n'
        print("GROUND:", Config().GROUND.temperature - 273.15, "°C")
        s+= "GROUND: "+ str(Config().GROUND.temperature - 273.15) + '\n'
        return s
    
    def update_temperature(self):
        walls = [wall for room in self.rooms for wall in room.walls.values()]
        HeatFlow.update_temperature(walls
                                    + [room.roof for room in self.rooms]
                                    + [room.floor for room in self.rooms]
                                    + [opening for wall in walls for opening in wall.openings])
    
    def update_visuals(self):
        for room in self.rooms:
            room.on_temperature_change()
    
  
    def generate_walls(self, room: Room, wall_layers):
        for direction in [Direction(axis, positive) for axis, positive in cartesian_product([Axis.X, Axis.Z], [True, False])]:
            height = room.dimensions[Axis.Y]
            wall_axis = Axis.X if direction.axis == Axis.Z else Axis.Z
            width = room.dimensions[wall_axis]
            x, z = 0, 0
            if direction.axis == Axis.X:
                x = room.dimensions[direction.axis]/2 if direction.positive else -room.dimensions[direction.axis]/2
            else:
                z = room.dimensions[direction.axis]/2 if direction.positive else -room.dimensions[direction.axis]/2
            wall = MultiLayerObject(Axis.Y, wall_axis, height, width, 20, wall_layers, border=([room, Config().ENVIRONMENT] if direction.positive else [Config().ENVIRONMENT, room]), openings=list(), 
                                               local_position=vector(x, 0, z), parent=room)
            room.walls[direction] = wall
            

    def add_openings(self, wall: MultiLayerObject, i: int):    
        if(len(wall.openings) == 0):
            #return
            wall.openings.append(MultiLayerObject(0.5, 0.5, 20, [(0.1, Material(1225, 1005, 0.024))], border=[wall, Config().ENVIRONMENT], local_position=vector(0, 0, 0), parent=None))
            wall.openings.append(MultiLayerObject(0.5, 0.5, 20, [(0.1, Material(1225, 1005, 0.024))], border=[wall, Config().ENVIRONMENT], local_position=vector(0, 0, 0), parent=None))
        num_openings = len(wall.openings)
        distance_between_openings = wall.axis2_length/(num_openings+1)
        initial_position = -wall.axis2_length/2 + distance_between_openings
        for j in range(num_openings):
            if(wall.openings[j].parent is not None):
                continue
            
            offset = initial_position + j*distance_between_openings
            x = 0 if i%2==1 else offset
            z = 0 if i%2==0 else offset
            wall.openings[j].local_position = vector(x, 0, z)
            wall.openings[j].set_parent(wall)
            wall.openings[j].make_box()
            if(i%2==1):
                wall.openings[j].shape.rotate(angle=pi/2, axis=vector(0, 1, 0))
        

