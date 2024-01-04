from .material import *

class ObjectLayer:
    def __init__(self, thickness, material : Material):
        self.thickness : float = thickness  # (m)
        self.material : Material = material