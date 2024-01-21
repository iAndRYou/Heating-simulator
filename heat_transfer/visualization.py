from vpython import *
from colorsys import hsv_to_rgb

#utility functions 
def tuple_to_vector(tup):
    return vector(tup[0], tup[1], tup[2])

class Object3D:
    local_position: vector
    global_position: vector
    size: vector
    parent: "Object3D"
    children: list["Object3D"]
    shape: box

    object_label: label

    def __init__(self, local_position: vector, dimensions: vector, parent: "Object3D" = None):
        self.local_position = local_position
        self.size = dimensions
        self.children = []
        self.shape = None
        self.set_parent(parent)
    
    def get_label(self) -> str | None:
        return None
    
    def get_temperature(self) -> float | None:
        return None
    
    def on_temperature_change(self):
        if self.shape:
            new_temperature = self.get_temperature()
            if new_temperature is not None:
                self.shape.color = self.map_temperature_to_color(new_temperature)
            new_label = self.get_label()
            if new_label is not None:
                self.object_label.text = new_label
        
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
        l = self.get_label()
        if l is not None:
            self.object_label = label(pos=self.global_position, text=l)

        if(temperature != None):
            color = self.map_temperature_to_color(temperature)
        self.shape = box(pos=self.global_position, size=self.size, opacity=opacity, color=color)
        
    def map_temperature_to_color(self, temperature_kelvin):
        temperature = temperature_kelvin - 273.15 # convert to celsius
        normalized_temperature = 0.6 - 0.6*(temperature + 20)/70 # temp scale from -10 to 40, accepted 0, 40
        h = normalized_temperature #(1 - normalized_temperature)  # H 
        s = 0.8  # Saturation
        v = 1.0  # Value
        
        color_rgb = hsv_to_rgb(h, s, v)
        return vector(color_rgb[0], color_rgb[1], color_rgb[2])
   