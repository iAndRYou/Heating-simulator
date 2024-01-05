from .generic import *
from .model_parameters import TIME_STEP
from .models.room import *
from math import exp


class Convection:
    @staticmethod
    def update_temperature(wall: MultiLayerObject):
        for bordering_object in wall.border:
            border_layer = wall.layers[0] # warstwa graniczna styczna z bordering_object?
            for node in border_layer.nodes:
                if prev_node is None:
                    prev_node = node
                    continue
            
                node_mass_heat_capacity = node.mass * node.material.specific_heat_capacity
                bordering_object_mass_heat_capacity = bordering_object.mass * bordering_object.material.specific_heat_capacity
                
                # node area?
                k_coeff = border_layer.material.conductivity * node.area * (1 / node_mass_heat_capacity + 1 / bordering_object_mass_heat_capacity) / border_layer.thickness
                                
                # Teq = (T1 + T2 * (m2c2 / m1c1)) / (1 + m2c2 / m1c1)
                equilibrium_temperature = (node.temperature + bordering_object.temperature * (bordering_object_mass_heat_capacity / node_mass_heat_capacity)) / (1 + bordering_object_mass_heat_capacity / node_mass_heat_capacity)
                
                node_new_temperature = equilibrium_temperature + (node.temperature - bordering_object.temperature) * (bordering_object_mass_heat_capacity / (node_mass_heat_capacity + bordering_object_mass_heat_capacity)) * exp(-k_coeff * TIME_STEP)
                bordering_object_new_temperature = equilibrium_temperature + (bordering_object.temperature - node.temperature) * (node_mass_heat_capacity / (node_mass_heat_capacity + bordering_object_mass_heat_capacity)) * exp(-k_coeff * TIME_STEP)