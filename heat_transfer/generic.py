from math import prod
from .model_parameters import Config
from enum import Enum

#visualization
from vpython import *
from colorsys import hsv_to_rgb

# from .models.object_layer import ObjectLayer

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


#visualization
class Object3D:
    local_position : vector
    global_position : vector
    size : vector
    parent : "Object3D"
    children : list["Object3D"]
    shape : box
    def __init__(self, local_position : vector, dimensions : vector, parent : "Object3D" = None):
        self.local_position = local_position
        self.size = dimensions
        self.children = []
        self.shape = None
        self.set_parent(parent)

        
    def update_position(self):
        if self.parent:
            self.global_position = self.parent.global_position + self.local_position
        else:
            self.global_position = self.local_position
        if self.shape:
            self.shape.pos = self.global_position
        self.update_children()
         
    def update_children(self):
        for child in self.children:
            child.update_position()   
            
    def set_parent(self, parent):
        self.parent = parent
        if parent != None and self not in parent.children and parent != self:
            parent.children.append(self) 
        self.update_position()     
    
    def set_position(self, position : vector):
        self.local_position = position
        self.update_position()
         
            
    def make_box(self, color=vector(255, 255, 255), temperature=None, opacity=0.8):
        if(temperature != None):
            color = self.map_temperature_to_color(temperature)
        self.shape = box(pos=self.global_position, size=self.size, opacity=opacity, color=color)
        
    def map_temperature_to_color(self, temperature_kelvin):
        temperature = temperature_kelvin - 273.15 # convert to celsius
        normalized_temperature = (temperature + 50) / 100 # temp scale from -50 to 50
        h = 1 * (1 - normalized_temperature)  # H 
        s = 0.8  # Saturation
        v = 1.0  # Value
        
        color_rgb = hsv_to_rgb(h, s, v)
        return vector(color_rgb[0], color_rgb[1], color_rgb[2])
   
    
            
#utility functions 
def tuple_to_vector(tup):
    return vector(tup[0], tup[1], tup[2])


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

    
class HeatingSystem:
    def __init__(self, name, power, temperature):
        self.name = name
        self.power = power
        self.temperature = temperature
    


class Material:
    density: float # kg/m^3
    specific_heat_capacity: float # J/(kg*K)
    conductivity: float # W/(m*K)

    def __init__(self, density: float, specific_heat_capacity: float, conductivity: float):
        self.density = density
        self.specific_heat_capacity = specific_heat_capacity
        self.conductivity = conductivity


class UniformTemperatureObject:
    temperature: float # K
    material: Material
    volume: float | None = None # m^3

    def __init__(self, temperature_celsius: float, material: Material, volume: float | None = None):
        self.temperature = temperature_celsius + 273.15
        self.material = material
        self.volume = volume

    @property
    def mass(self) -> float:
        return self.volume * self.material.density

    def update_temperature(self, heat: int):
        if self.volume is not None:
            self.temperature += heat / (self.material.specific_heat_capacity * self.mass)

        # else:  infinite heat capacity -> temperature does not change

