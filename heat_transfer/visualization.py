from typing import Any
from vpython import *
from colorsys import hsv_to_rgb
from heat_transfer.model_parameters import Config

#utility functions 
def tuple_to_vector(tup):
    return vector(tup[0], tup[1], tup[2])


class Scene:
    scene: canvas = scene

    def __init__(self, temperature_text_update_callback):
        self.scene.title = "Heat transfer"
        self.scene.append_to_caption('\nEnvironment temperature\n')
        self.slider_env_temp = slider(min=-30, max=60, value=(Config().ENVIRONMENT.temperature - 273.15), length=220, bind=self.set_temp_env, right=15)
        self.temp_text = wtext(text='{:.2f}'.format(self.slider_env_temp.value))
        self.scene.append_to_caption('\u00b0 Celsius\n')

        self.scene.append_to_caption('Ground temperature\n')
        self.slider_ground_temp = slider(min=-30, max=60, value=(Config().GROUND.temperature - 273.15), length=220, bind=self.set_temp_ground, right=15)
        self.temp_ground_text = wtext(text='{:.2f}'.format(self.slider_ground_temp.value))
        self.scene.append_to_caption('\u00b0 Celsius\n')

        self.scene.append_to_caption('Target room temperature\n')
        self.slider_target_temp = slider(min=-30, max=60, value=(Config().TARGET_TEMPERATURE - 273.15), length=220, bind=self.set_temp_target, right=15)
        self.temp_target_text = wtext(text='{:.2f}'.format(self.slider_target_temp.value))
        self.scene.append_to_caption('\u00b0 Celsius\n')

        self.temperature_text_callback = temperature_text_update_callback
        self.temperature_text = wtext(text=temperature_text_update_callback())
        self.time_elapsed_text = wtext(text="0 hours passed")

    def set_temp_env(self):
        self.temp_text.text = '{:.2f}'.format(self.slider_env_temp.value)

    def set_temp_ground(self):
        self.temp_ground_text.text = '{:.2f}'.format(self.slider_ground_temp.value)
    
    def set_temp_target(self):
        self.temp_target_text.text = '{:.2f}'.format(self.slider_target_temp.value)

    def update_scene(self):
        Config().ENVIRONMENT.temperature = self.slider_env_temp.value + 273.15
        Config().GROUND.temperature = self.slider_ground_temp.value + 273.15
        Config().TARGET_TEMPERATURE = self.slider_target_temp.value + 273.15

    def update_slider_values(self):
        self.slider_env_temp.value = Config().ENVIRONMENT.temperature - 273.15
        self.slider_ground_temp.value = Config().GROUND.temperature - 273.15
        self.slider_target_temp.value = Config().TARGET_TEMPERATURE - 273.15
        self.set_temp_env()
        self.set_temp_ground()
        self.set_temp_target()


    def update_text(self, hours_passed):
        self.temperature_text.text = self.temperature_text_callback()
        self.time_elapsed_text.text = f"{hours_passed} hours passed"


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
   