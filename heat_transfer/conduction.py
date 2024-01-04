from typing import List, Dict, Tuple, Any
from .generic import *
from .model_parameters import *


class Conduction:
    @staticmethod
    def update_temperature(multilayer_object: MultiLayerObject):
        prev_node = None
        for layer in multilayer_object.layers:
            for node in layer.nodes:
                if prev_node is None:
                    prev_node = node
                    continue

                heat_flux = layer.material.conductivity * (node.temperature - prev_node.temperature) / NODE_DISTANCE
                prev_node.heat_flow(heat_flux * TIME_STEP * multilayer_object.area)
                node.heat_flow(-heat_flux * TIME_STEP * multilayer_object.area)
                
                prev_node = node
