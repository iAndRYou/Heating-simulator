from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.generic import *
from heat_transfer.model_parameters import Config
from heat_transfer.models.heating_systems import *
from matplotlib import pyplot as plt
import numpy as np
from vpython import *



class Plot:
    def __init__(self, rooms: list[Room]):
        self.fig, self.ax = plt.subplots()

        self.rooms = rooms
        self.x_data = []
        self.y_data = {room.id: [] for room in rooms}
        self.lines = {room.id: self.ax.plot(self.x_data, self.y_data[room.id], '-')[0] for room in rooms}

        # Set plot limits
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 50)
        self.ax.set_xlabel("Time [h]")
        self.ax.set_ylabel("Temperature [°C]")
        # set legend
        self.ax.legend([f"Room {room.id}" for room in rooms])
    
    def update(self, hours_passed: int):
        self.x_data.append(hours_passed)
        for room in self.rooms:
            self.y_data[room.id].append(room.temperature - 273.15)

            # Update plot
            self.lines[room.id].set_xdata(self.x_data)
            self.lines[room.id].set_ydata(self.y_data[room.id])

        self.ax.relim()
        self.ax.autoscale_view()

        # Refresh the plot
        plt.draw()
        plt.pause(0.5)



# x - szerokość, y -wysokość, z - długość
#### SCENE CONFIG START
config = Config()
def set_temp_env():
    temp_text.text = '{:1.1f}'.format(slider_env_temp.value)
def set_temp_ground():
    temp_ground_text.text = '{:1.1f}'.format(slider_ground_temp.value)


scene.title = "Heat transfer"
scene.append_to_caption('\nEnvironment temperature\n')
slider_env_temp = slider(min=-30, max=60, value=(config.ENVIRONMENT.temperature - 273.15), length=220, bind=set_temp_env, right=15)
temp_text = wtext(text='{:1.1f}'.format(slider_env_temp.value))
scene.append_to_caption('\u00b0 Celsius\n')

scene.append_to_caption('Ground temperature\n')
slider_ground_temp = slider(min=-30, max=60, value=(config.GROUND.temperature - 273.15), length=220, bind=set_temp_ground, right=15)
temp_ground_text = wtext(text='{:1.1f}'.format(slider_ground_temp.value))
scene.append_to_caption('\u00b0 Celsius\n')

scene.append_to_caption('\nLOGS:\n')

    
def scene_update():
    config.ENVIRONMENT.temperature = slider_env_temp.value + 273.15
    config.GROUND.temperature = slider_ground_temp.value + 273.15
    
#### SCENE CONFIG END

room1 = Room(1,
             (3, 4, 3), 
             13,
             vector(4.5, 0, 0),
             parent=None)

room2 = Room(2,
            (6, 4, 3),
            25,
            vector(0, 0, 0),
            parent=None)

room3 = Room(3,
            (6, 4, 3),
            40,
            vector(0, 0, 3),
            parent=None)

heating_system = RadiatorHeating(rooms=[room1, room2, room3])

house = House([room1, room2, room3],
              interfaces=[[[room2, room1], Direction(Axis.X, True)], [[room2, room3], Direction(Axis.Z, True)]],
              wall_layers=[(0.1, Material(2500, 800, 1.4))],
              roof_layers=[(0.1, Material(2500, 800, 1.4))],
              floor_layers=[(0.1, Material(2500, 800, 1.4))],
              heating_system=heating_system,
              local_position=vector(0, 0, 0))


room1.make_box(temperature=room1.temperature)
room2.make_box(temperature=room2.temperature)
room3.make_box(temperature=room3.temperature)



room1.add_windows(Direction(Axis.Z, False), 1)
room1.add_windows(Direction(Axis.Z, True), 1)
room1.add_windows(Direction(Axis.X, True), 1)
room1.add_door(Direction(Axis.X, False))

room2.add_door(Direction(Axis.Z, True))
room2.add_windows(Direction(Axis.Z, False), 2)
room2.add_windows(Direction(Axis.X, False), 1)

room3.add_windows(Direction(Axis.Z, True), 2)
room3.add_windows(Direction(Axis.X, True), 1)
room3.add_windows(Direction(Axis.X, False), 1)

room1.visualize_openings()
room2.visualize_openings()
room3.visualize_openings()


plot = Plot(rooms=[room1, room2, room3])

room_temp_text = wtext(text=house.print_rooms_temperatures())
time_elapsed_text = wtext(text="0 hours passed")
# node_temperatures1 = [node.temperature for node in house.rooms[0].walls[0].nodes

room_temperature_logs = {room.id: [room.temperature] for room in house.rooms}
UPDATE_STEP = 3 # in hours

for i in range(50):
    for __ in range(UPDATE_STEP * 3600 // Config().TIME_STEP):
        house.update_temperature()
        scene_update()
    house.update_visuals()
    room_temp_text.text = house.print_rooms_temperatures()
    plot.update(UPDATE_STEP*(i+1))
    time_elapsed_text.text = str(UPDATE_STEP*(i+1))+" hours passed"
    print(UPDATE_STEP*(i+1), "hours passed")

plt.show()
input()


