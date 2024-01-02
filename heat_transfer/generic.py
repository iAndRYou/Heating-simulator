class MultiLayerObject:
    def __init__(self, layers, temperature_1, temperature_2):
        self.layers : List[ObjectLayer] = layers  
        self.temperature_1 : float = temperature_1  
        self.temperature_2 : float = temperature_2
        
    @property   
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)

    def get_surface_area(self):
        return 0
    

class Opening(MultiLayerObject):
    def get_surface_area(self):
        return 0
    
class HeatingSystem:
    def __init__(self, name, power, temperature):
        self.name = name
        self.power = power
        self.temperature = temperature
    

    
