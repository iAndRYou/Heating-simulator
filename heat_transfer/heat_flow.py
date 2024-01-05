from typing import List, Dict, Tuple, Any
from .generic import *
from .model_parameters import *
from .models.room import *

class HeatFlow:
    @staticmethod
    def update_temperature_at_interface(interface: MultiLayerObject):
        prev_node = None
        node_heat = {node: 0 for node in interface.nodes} # net heat for wall nodes
        border_heat = {border: 0 for border in interface.border} # net heat for bordering objects

        for layer in interface.layers:
            for node in layer.nodes:
                if prev_node is None:
                    prev_node = node
                    continue

                heat_flux = Conduction.heat_flux(prev_node, node, layer.material, NODE_DISTANCE)
                heat = heat_flux * TIME_STEP * interface.area

                node_heat[node] -= heat
                node_heat[prev_node] += heat

                prev_node = node


        for bordering_air, bordering_node in ((interface.border[0], interface.layers[0].nodes[0]), (interface.border[1], interface.layers[-1].nodes[-1])):
            heat_flux = Convection.heat_flux(bordering_node, bordering_air, interface.height)
            heat = heat_flux * TIME_STEP * interface.area

            node_heat[bordering_node] -= heat
            border_heat[bordering_air] += heat
        
        for node in node_heat:
            node.update_temperature(node_heat[node])

        for border in border_heat:
            border.update_temperature(border_heat[border])


class Conduction:
    @staticmethod
    def heat_flux(node1: UniformTemperatureObject, node2: UniformTemperatureObject, material: Material, distance: float):
            heat_flux = material.conductivity * (node2.temperature - node1.temperature) / distance

            return heat_flux


class Convection:
    @staticmethod
    def heat_flux(bordering_node: UniformTemperatureObject, bordering_air: UniformTemperatureObject, characteristic_length: float):
        # assumptions for grashof number calculation:
        # k = 0.026 W/(m*K)
        # kinematic viscosity = 1.5 * 10^-5 m^2/s
        # g = 9.81 m/s^2
        # specific heat = 1005 J/(kg*K)
        # thermal expansion coefficient is the inverse of the temperature in K
        # characteristic length = height of the wall

        prandtl_number = 0.71
        grashof_number = 88979591837 * characteristic_length**3 * abs(bordering_node.temperature - bordering_air.temperature) / bordering_air.temperature 
        
        rayleigh_number = grashof_number * prandtl_number

        # assumptions for nusselt number calculation:
        # 10^4 < Ra < 10^9
        # => constants C=0.59 and n=0.25

        nusselt_number = 0.59 * rayleigh_number**0.25

        heat_transfer_coefficient = nusselt_number * AIR.conductivity / characteristic_length

        heat_flux = heat_transfer_coefficient * (bordering_node.temperature - bordering_air.temperature)

        return heat_flux