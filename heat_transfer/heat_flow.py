from .generic import *
from .model_parameters import Config
from .models.room import *
from .models.layered_objects import MultiLayerObject
import numpy as np


class HeatFlow:
    @staticmethod
    def update_temperature(heating_system: HeatingSystem, interfaces: list[MultiLayerObject]):
        object_heat: dict[UniformTemperatureObject, float] = dict()

        object_heat.update(heating_system.heat_flow())

        for interface in interfaces:
            for object, heat in HeatFlow.update_temperature_at_interface(interface).items():
                if object in object_heat:
                    object_heat[object] += heat
                else:
                    object_heat[object] = heat

        for object, heat in object_heat.items():
            object.update_temperature(heat)
            if object.temperature < 0:
                print("temperature < 0")
                print("interface:", interfaces)
                print("object:", object)
                print("heat:", heat)
                print("object_heat:", object_heat)
                exit()

    @staticmethod
    def update_temperature_at_interface(interface: MultiLayerObject):
        prev_node = None
        object_heat: dict[UniformTemperatureObject, float] = dict()
        object_heat.update({node: 0 for node in interface.nodes}) # net heat for wall nodes
        object_heat.update({border: 0 for border in interface.border}) # net heat for bordering objects

        # conduction through the interface
        for layer in interface.layers:
            for node in layer.nodes:
                if prev_node is None:
                    prev_node = node
                    continue

                heat_flux = Conduction.heat_flux(prev_node, node, Config().NODE_DISTANCE, layer.material)
                heat = heat_flux * Config().TIME_STEP * interface.area

                object_heat[node] -= heat
                object_heat[prev_node] += heat

                prev_node = node


        border1_object = interface.border[0]
        border1_outer_node = interface.layers[0].nodes[0]
        border2_object = interface.border[-1]
        border2_outer_node = interface.layers[-1].nodes[-1]

        border1_isair = isinstance(border1_object, Room) or (border1_object == Config().ENVIRONMENT)
        border2_isair = isinstance(border2_object, Room) or (border2_object == Config().ENVIRONMENT)


        if border1_isair:
            bordering_air = border1_object
            bordering_node = border1_outer_node
            heat_flux = Convection.heat_flux(bordering_node, bordering_air, interface.axis1_length)
            heat = heat_flux * Config().TIME_STEP * interface.area

            object_heat[bordering_node] -= heat
            object_heat[bordering_air] += heat
        else:
            heat_flux = Conduction.heat_flux(border1_outer_node, border1_object, Config().NODE_DISTANCE)
            heat = heat_flux * Config().TIME_STEP * interface.area

            object_heat[border1_object] -= heat
            object_heat[border1_outer_node] += heat


        if border2_isair:
            bordering_air = border2_object
            bordering_node = border2_outer_node
            heat_flux = Convection.heat_flux(bordering_node, bordering_air, interface.axis1_length)
            heat = heat_flux * Config().TIME_STEP * interface.area

            object_heat[bordering_node] -= heat
            object_heat[bordering_air] += heat
        else:
            heat_flux = Conduction.heat_flux(border2_outer_node, border2_object, Config().NODE_DISTANCE)
            heat = heat_flux * Config().TIME_STEP * interface.area

            object_heat[border2_object] -= heat
            object_heat[border2_outer_node] += heat
        
        return object_heat


class Conduction:
    @staticmethod
    def heat_flux(node1: UniformTemperatureObject, node2: UniformTemperatureObject, distance: float, material: Material | None = None):
        if material is None:
            conductivity = (node1.material.conductivity + node2.material.conductivity) / 2
        else:
            conductivity = material.conductivity

        heat_flux = conductivity * (node2.temperature - node1.temperature) / distance


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

        heat_transfer_coefficient = nusselt_number * Config().AIR.conductivity / characteristic_length

        heat_flux = heat_transfer_coefficient * (bordering_node.temperature - bordering_air.temperature)

        return heat_flux