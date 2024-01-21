from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.generic import *
from heat_transfer.model_parameters import Config
from matplotlib import pyplot as plt
import numpy as np
from vpython import *

# fig, ax = plt.subplots(1, 1)
# ax.set_aspect('equal')
# ax.set_xlim(0, 100)
# ax.set_ylim(0, 100)
# # ax.hold(True)
# plt.show(False)
# plt.draw()
# background = fig.canvas.copy_from_bbox(ax.bbox)
# x, y = 0, 0
# points_ = ax.plot(x, y, 'o')[0]

# def plot_temperature_logs(hours_passed: int, room_temperature: float):
#     # for i, temperature_log in enumerate(temperature_logs):
#     #     plt.plot(temperature_log, label=f"room {i+1}")
#     points_.set_data((hours_passed, room_temperature))
#     # restore background
#     fig.canvas.restore_region(background)

#     # redraw just the points
#     ax.draw_artist(points_)

#     # fill in the axes rectangle
#     fig.canvas.blit(ax.bbox)


# x - szerokość, y -wysokość, z - długość
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


house = House([room1, room2, room3],
              interfaces=[[[room2, room1], Direction(Axis.X, True)], [[room2, room3], Direction(Axis.Z, True)]],
              wall_layers=[(0.1, Material(2500, 800, 1.4))],
              roof_layers=[(0.1, Material(2500, 800, 1.4))],
              floor_layers=[(0.1, Material(2500, 800, 1.4))],
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


house.print_rooms_temperatures()
# node_temperatures1 = [node.temperature for node in house.rooms[0].walls[0].nodes

room_temperature_logs = [[room.temperature] for room in house.rooms]
UPDATE_STEP = 3 # in hours

for i in range(50):
    for __ in range(UPDATE_STEP * 3600 // Config().TIME_STEP):
        house.update_temperature()

    house.update_visuals()
    house.print_rooms_temperatures()
    # plot_temperature_logs(UPDATE_STEP*(i+1), room1.temperature - 273.15)
    print(UPDATE_STEP*(i+1), "hours passed")

plt.show()
input()