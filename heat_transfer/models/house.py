from .room import *
from ..generic import MultiLayerObject, Material, UniformTemperatureObject
from ..heat_flow import HeatFlow


def reverse_direction(direction):
    return (direction+2) if direction%2==direction else (direction-2)

class House(Object3D):
    rooms: list[Room]
    room_connections: dict[Room, list[tuple[Room, int]]] = dict()

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
            room.roof = MultiLayerObject(room.dimensions[0], room.dimensions[1], 20, roof_layers, border=[room, ENVIRONMENT])
            room.floor = MultiLayerObject(room.dimensions[0], room.dimensions[1], 20, floor_layers, border=[GROUND, room])
        
        for room in self.rooms:
            for room2, direction in self.room_connections[room]:
                room.walls[direction].border = [room, room2]
                room2.walls[reverse_direction(direction)] = room.walls[direction]

    
    def print_rooms_temperatures(self):
        print("ROOMS:")
        for room in self.rooms:
            print(room.temperature - 273.15, "°C")
        print("ENVIRONMENT:", ENVIRONMENT.temperature - 273.15, "°C")
        print("GROUND:", GROUND.temperature - 273.15, "°C")
    
    def update_temperature(self):
        for room in self.rooms:
            for wall in room.walls:
                HeatFlow.update_temperature_at_interface(wall)
            room.on_temperature_change()
    
  
    def generate_walls(self, room : Room, wall_layers):
        for i in range(4):
            height = room.dimensions[2]
            width = room.dimensions[i%2]
            offset_value = room.dimensions[(i+1)%2]/2
            x = 0 if i%2==0 else offset_value
            z = 0 if i%2==1 else offset_value
            z *= -1 if i>1 else 1
            x *= -1 if i>1 else 1
            wall = MultiLayerObject(room.dimensions[2], room.dimensions[i%2], 20, wall_layers, border=([room, ENVIRONMENT] if i<2 else [ENVIRONMENT, room]), openings=[], 
                                               local_position=vector(x, 0, z), parent=room)
            print("new wall", wall.openings)
            room.walls.append(wall)
            self.add_openings(wall, i)
            

    def add_openings(self, wall : MultiLayerObject, i : int):    
        if(len(wall.openings) == 0):
            #return
            wall.openings.append(MultiLayerObject(0.5, 0.5, 20, [(0.1, Material(1225, 1005, 0.024))], border=[wall, ENVIRONMENT], local_position=vector(0, 0, 0), parent=None))
            wall.openings.append(MultiLayerObject(0.5, 0.5, 20, [(0.1, Material(1225, 1005, 0.024))], border=[wall, ENVIRONMENT], local_position=vector(0, 0, 0), parent=None))
        num_openings = len(wall.openings)
        distance_between_openings = wall.width/(num_openings+1)
        initial_position = -wall.width/2 + distance_between_openings
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
        