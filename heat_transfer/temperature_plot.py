from heat_transfer.models.room import *
from heat_transfer.models.house import *
from heat_transfer.generic import *
from heat_transfer.model_parameters import Config
from heat_transfer.models.heating_systems import *
from matplotlib import pyplot as plt
import numpy as np
from vpython import *


class Plot:
    def __init__(self, rooms: list[Room], max_hours: int = 100):
        self.fig, self.ax = plt.subplots()

        self.rooms = rooms
        self.hours_passed = []
        self.room_temperature_log = {room.id: [] for room in rooms}
        self.room_lines = {room.id: self.ax.plot(self.hours_passed, self.room_temperature_log[room.id], '-')[0] for room in rooms}
        self.environment_temperature_log = []
        self.environment_line = self.ax.plot(self.hours_passed, self.environment_temperature_log, 'k-')[0]

        # Set plot limits
        self.ax.set_xlim(0, max_hours)
        self.ax.set_ylim(-10, 40)
        self.ax.set_xticks(np.arange(0, max_hours+1, 24))
        self.ax.set_xlabel("Time [h]")
        self.ax.set_ylabel("Temperature [°C]")
        # set legend
        self.ax.legend([f"Room {room.id}" for room in rooms] + ["Environment"])
        # grid
        self.ax.grid(True)
    
    def update(self, hours_passed: int):
        self.hours_passed.append(hours_passed)
        for room in self.rooms:
            self.room_temperature_log[room.id].append(room.temperature - 273.15)

            # Update plot
            self.room_lines[room.id].set_xdata(self.hours_passed)
            self.room_lines[room.id].set_ydata(self.room_temperature_log[room.id])
        
        self.environment_temperature_log.append(Config().ENVIRONMENT.temperature - 273.15)
        self.environment_line.set_xdata(self.hours_passed)
        self.environment_line.set_ydata(self.environment_temperature_log)

        self.ax.relim()
        self.ax.autoscale_view()

        # Refresh the plot
        plt.draw()
        plt.pause(2)