from ..generic import UniformTemperatureObject, Material
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

        self.nodes = [UniformTemperatureObject(init_temperature_celsius, material, self.parent_object.area*Config().NODE_DISTANCE) for _ in range(int(thickness // Config().NODE_DISTANCE))]


class MultiLayerObject(Object3D):
    layers: list[ObjectLayer]
    height: float
    width: float
    border: list["UniformTemperatureObject"]

    def __init__(self, height, width, init_temperature_celsius: float, layers: list[list[float, "Material"]], border: list["UniformTemperatureObject"], openings: list["MultiLayerObject"] = list(), #dict[tuple[float, float], "MultiLayerObject"] = dict(),
                local_position = vector(0, 0, 0), parent: "Object3D" = None):
        self.height = height
        self.width = width
        self.layers: list[ObjectLayer] = [ObjectLayer(init_temperature_celsius, thickness, material, self) for thickness, material in layers]
        self.openings = openings
        self.border = border
        super().__init__(dimensions=vector(self.width, self.height, self.thickness), local_position=local_position, parent=parent)
        
    @property   
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)
    
    @property
    def area(self):
        return self.height * self.width

    @property
    def nodes(self):
        return [node for layer in self.layers for node in layer.nodes]
