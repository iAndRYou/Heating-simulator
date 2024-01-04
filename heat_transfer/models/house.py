from .room import *
from ..generic import MultiLayerObject, Material, UniformTemperatureObject


def reverse_direction(direction):
    return (direction+2) if direction%2==direction else (direction-2)

class House:
    rooms: list[Room]
    room_connections: dict[Room, list[tuple[Room, int]]] = dict()

    def __init__(self, rooms: list[Room], interfaces, wall_layers, roof_layers, floor_layers):
        self.rooms = rooms

        visited_interfaces = set()
        for room in self.rooms:
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
            room.walls = [MultiLayerObject(room.dimensions[2], room.dimensions[i%2], 20, wall_layers, border=([room, ENVIRONMENT] if i<2 else [ENVIRONMENT, room])) for i in range(4)]
            room.roof = MultiLayerObject(room.dimensions[0], room.dimensions[1], 20, roof_layers, border=[room, ENVIRONMENT])
            room.floor = MultiLayerObject(room.dimensions[0], room.dimensions[1], 20, floor_layers, border=[GROUND, room])
        
        for room in self.rooms:
            for room2, direction in self.room_connections[room]:
                room.walls[direction].border = [room, room2]
                room2.walls[reverse_direction(direction)] = room.walls[direction]

    