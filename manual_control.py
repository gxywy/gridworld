import sys
import numpy as np
from gridwolrd import GridWorld
from window import Window

def reset():
	state = env.reset()
	window.show_grid(state)

def step(action):
	state, reward, done = env.step(action)
	print('action=%d, reward=%.2f' % (action, reward))

	if done:
		print('done!')
		reset()
	else:
		window.show_grid(state)

def key_handler(event):
	print('pressed', event.key)

	if event.key == 'escape':
		window.close()
		return

	if event.key == 'backspace':
		reset()
		return

	if event.key == 'up':
		step(env.actions.up)
		return
	if event.key == 'down':
		step(env.actions.down)
		return
	if event.key == 'left':
		step(env.actions.left)
		return
	if event.key == 'right':
		step(env.actions.right)
		return

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		env = GridWorld((int(sys.argv[1]), int(sys.argv[2])))
	else:
		env = GridWorld()
		file = input("grid file (default None):")
		if file is not None:
			env.load_file(file.replace("\\", "/").replace("\"", ""))
	
	window = Window()
	window.reg_key_handler(key_handler)

	reset()

	# Blocking event loop
	window.show(block=True)