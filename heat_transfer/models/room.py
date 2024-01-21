from .layered_objects import MultiLayerObject
from ..generic import *
from ..model_parameters import Config



class Room(UniformTemperatureObject, Object3D):
    id: int
    dimensions: tuple[float, float, float]
    walls: dict[Direction, MultiLayerObject]
    roof: MultiLayerObject
    floor: MultiLayerObject

    def __init__(self, id, dimensions, init_temperature_celsius,
                 local_position = vector(0, 0, 0), parent: "Object3D" = None):
        super().__init__(init_temperature_celsius, Config().AIR, prod(dimensions), object_type="room")

        self.dimensions = dimensions
        self.walls = dict()
        self.id = id
        self.roof = None
        self.floor = None
        Object3D.__init__(self, dimensions=tuple_to_vector(dimensions), local_position=local_position, parent=parent)

    def add_windows(self, direction: Direction, n: int):
        wall = self.walls[direction]
        wall_axis = Axis.X if direction.axis == Axis.Z else Axis.Z
        for width_pos in [wall.dimensions[wall_axis]*(i/(n+1) - 1/2) for i in range(1, n+1)]:
            position = [0, wall.dimensions[Axis.Y]*(2/3 - 1/2), 0]
            position[wall_axis] = width_pos
            wall.add_window(position=position, size=(0.8, 0.8))
    
    def add_door(self, direction: Direction):
        wall = self.walls[direction]
        wall_axis = Axis.X if direction.axis == Axis.Z else Axis.Z
        size = [2, 1]
        position = [0, (1/2)*size[0]-(1/2)*wall.dimensions[Axis.Y], 0]

        wall.add_door(position=position, size=size)
    
    def visualize_openings(self):
        for wall in self.walls.values():
            wall.visualize_openings()

    def get_label(self):
        return f"Room {self.id}: {self.temperature - 273.15:.2f} C"

    def get_temperature(self):
        return self.temperature