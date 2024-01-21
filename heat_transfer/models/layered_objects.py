from ..generic import UniformTemperatureObject, Material, Axis
from ..visualization import Object3D
from ..model_parameters import Config

from vpython import vector

class ObjectLayer:
    thickness: float
    material: "Material"
    parent_object: "MultiLayerObject"
    nodes: list["UniformTemperatureObject"]

    def __init__(self, init_temperature_celsius: float, thickness: float, material: "Material", parent_object: "MultiLayerObject"):
        self.thickness = thickness
        self.material = material
        self.parent_object = parent_object

        self.nodes = [UniformTemperatureObject(init_temperature_celsius, material, self.parent_object.area*Config().NODE_DISTANCE, object_type="node") for _ in range(int(thickness // Config().NODE_DISTANCE))]


class MultiLayerObject(Object3D):
    layers: list[ObjectLayer]
    axis1: Axis
    axis2: Axis
    axis1_length: float
    axis2_length: float
    border: list["UniformTemperatureObject"]

    def __init__(self, axis1, axis2, axis1_length, axis2_length, init_temperature_celsius: float, layers: list[list[float, "Material"]], border: list["UniformTemperatureObject"], openings: list["MultiLayerObject"] = list(), #dict[tuple[float, float], "MultiLayerObject"] = dict(),
                local_position = vector(0, 0, 0), parent: "Object3D" = None):
        self.axis1 = axis1
        self.axis2 = axis2
        self.axis1_length = axis1_length
        self.axis2_length = axis2_length
        self.openings = openings
        self.init_temperature_celsius = init_temperature_celsius
        self.layers: list[ObjectLayer] = [ObjectLayer(init_temperature_celsius, thickness, material, self) for thickness, material in layers]
        self.border = border
        super().__init__(dimensions=vector(*self.dimensions), local_position=local_position, parent=parent)

        for opening in openings:
            opening.parent = self
        
    @property   
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)
    
    @property
    def area(self):
        return self.axis1_length * self.axis2_length - sum(opening.area for opening in self.openings)

    @property
    def nodes(self):
        return [node for layer in self.layers for node in layer.nodes]

    @property
    def dimensions(self):
        axis_to_length = {self.axis1: self.axis1_length, self.axis2: self.axis2_length}
        return [axis_to_length.get(axis, self.thickness) for axis in Axis]


    def add_window(self, position: tuple[float], size: tuple[float, float]):
        window = MultiLayerObject(self.axis1, 
                                  self.axis2, 
                                  *size,
                                  self.init_temperature_celsius,
                                  [[0.07, Config().GLASS]], 
                                  border=self.border,
                                  local_position=vector(*position),
                                  parent=self)
                                  
        self.openings.append(window) 
        
        self.layers = [ObjectLayer(self.init_temperature_celsius, layer.thickness, layer.material, self) for layer in self.layers]

    def add_door(self, position: tuple[float], size: tuple[float, float]):
        door = MultiLayerObject(self.axis1, 
                                  self.axis2, 
                                  *size,
                                  self.init_temperature_celsius,
                                  [[0.07, Config().WOOD]], 
                                  border=self.border,
                                  local_position=vector(*position),
                                  parent=self)
                                  
        self.openings.append(door) 
        
        self.layers = [ObjectLayer(self.init_temperature_celsius, layer.thickness, layer.material, self) for layer in self.layers]
    
    def visualize_openings(self):
        for opening in self.openings:
            opening.make_box(color=vector(0, 0, 0))