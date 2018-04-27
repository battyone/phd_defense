"""Demo of spikes and filtering"""
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Spikes():
    def __init__(self, ax, window=2, t_max=5, dt=0.01):
        self.ax = ax
        self.dt = dt
        self.w_size = window

        self.t_data = np.arange(0, 2*t_max, dt)
        self.y_data = np.random.sample(len(self.t_data))

        self.line = Line2D([], [])
        self.ax.add_line(self.line)

        self._reset()

    def _reset(self):
        """Reset the animation state"""
        self.w_idx = np.array([0, 1], dtype=int)
        self.t_display = [self.t_data[0]]
        self.y_display = [self.y_data[0]]
        self.ax.set_xlim(0, self.w_size)

    # def update(self, w_idx, w_update):
    def update(self, w_params):
        """Update the animation"""
        w_idx, w_update = w_params
        self.t_display = self.t_data[w_idx[0]:w_idx[1]]
        self.y_display = self.y_data[w_idx[0]:w_idx[1]]
        self.line.set_data(self.t_display, self.y_display)
        if w_update:
            self.ax.set_xlim(self.t_display[0], self.t_display[-1])
        self.ax.figure.canvas.draw()
        return self.line,

    def w_idx_generator(self):
        while self.t_display[-1] != self.t_data[-1]:
            if self.t_display[-1]-self.t_display[0] < self.w_size:
                self.w_idx[1] += 1
                update_window = False
            else:
                self.w_idx += 1
                update_window = True
            yield (self.w_idx, update_window)
        self._reset()

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
spikes = Spikes(ax)

interval_ms = spikes.dt*1E3
ani = animation.FuncAnimation(
    fig, spikes.update, spikes.w_idx_generator, interval=interval_ms, blit=True, repeat=False)

# ani.save("test.gif", dpi=80, writer="imagemagick")
ani.save("test.mp4", fps=30, extra_args=['-vcodec', 'libx264'])
# plt.show()
