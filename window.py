import sys
import matplotlib.pyplot as plt
import matplotlib as mpl

class Window:
	def __init__(self):
		self.fig, self.ax = plt.subplots()
		self.fig.canvas.set_window_title("gridworld")
		self.cmap = mpl.colors.ListedColormap(['black', 'red', 'green', 'cyan'])

		self.ax.set_xticks([], [])
		self.ax.set_yticks([], [])

		self.closed = False

		def close_handler(evt):
			self.closed = True
		self.fig.canvas.mpl_connect('close_event', close_handler)

	def show_grid(self, grid):
		self.ax.imshow(grid, cmap=self.cmap)
		self.fig.canvas.draw()

		# Let matplotlib process UI events
		# This is needed for interactive mode to work properly
		plt.pause(0.001)

	def reg_key_handler(self, key_handler):
		self.fig.canvas.mpl_connect('key_press_event', key_handler)

	def show(self, block=True):
		# If not blocking, trigger interactive mode
		if not block:
			plt.ion()

		# Show the plot
		# In non-interative mode, this enters the matplotlib event loop
		# In interactive mode, this call does not block
		plt.show()

	def close(self):
		plt.close()