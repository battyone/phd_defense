"""Demo of spikes and filtering"""
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Spikes():
    def __init__(self, ax, window=2, t_max=5, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.t_max = t_max
        self.t_data = np.arange(0, 2*t_max, dt)
        self.y_data = np.random.sample(len(self.t_data))

        self.t_display = [self.t_data[0]]
        self.y_display = [self.y_data[0]]

        self.line = Line2D(self.t_display, self.y_display)
        self.ax.add_line(self.line)
        self.w_idx = np.array([0, 1], dtype=int) # window indices
        self.window = [0, window]
        self.ax.set_xlim(self.window[0], self.window[1])

    def update(self, y):
        if self.t_display[-1] < self.window[1]:
            self.w_idx[1] += 1
            self.t_display = self.t_data[self.w_idx[0]:self.w_idx[1]]
            self.y_display = self.y_data[self.w_idx[0]:self.w_idx[1]]
        else:
            self.w_idx += 1
            self.t_display = self.t_data[self.w_idx[0]:self.w_idx[1]]
            self.y_display = self.y_data[self.w_idx[0]:self.w_idx[1]]
            self.window[0] = self.t_display[0]
            self.window[1] = self.t_display[1]
            self.ax.set_xlim(self.window[0], self.window[1])

        self.line.set_data(self.t_display, self.y_display)
        self.ax.figure.canvas.draw()
        return self.line,

    def get_framecount(self):
        framecount = int(np.ceil(self.t_max/self.dt))
        return framecount

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
spikes = Spikes(ax)

ani = animation.FuncAnimation(
    fig, spikes.update, spikes.get_framecount(), interval=10, blit=True)

plt.show()
