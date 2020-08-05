from argparse import Action
import numpy as np
from enum import IntEnum

class GridWorld:

	def __init__(self, size=(5, 5)):
		assert len(size) == 2, "input x and y"
		assert size[0] > 0 and size[1] > 0, "input positive number"

		self.height = size[0]
		self.width = size[1]
		self.goal = (self.height - 1, self.width - 1)
		self.pos = [0, 0]

		# initialize grid
		self.grid = np.zeros((self.height, self.width))
		self.grid[self.goal] = 2
		self.done = False

		class Actions(IntEnum):
			up = 0
			down = 1
			left = 2
			right = 3
		self.actions = Actions

	def reset(self, random_agent=False, random_goal=False):
		'''
			observation: agent: 1
						 goal: 2
						 wall: -1
						 else: 0
		'''
		
		self.grid[self.grid == 1] = 0
		self.grid[self.grid == 2] = 0
		
		if random_agent is True:
			# random agent position
			random_pos = np.random.randint(self.height * self.width - 1)
			self.pos = [random_pos // self.height, random_pos % self.width]
		else:
			self.pos = [0, 0]
		
		if random_goal is True:
			# random goal position
			random_goal = np.random.randint(self.height * self.width - 1)
			self.goal = (random_goal // self.height, random_goal % self.width)
		else:
			self.goal = (self.height - 1, self.width - 1)

		self.grid[self.pos[0], self.pos[1]] = 1
		self.grid[self.goal] = 2
		self.done = False

		return self.grid

	def step(self, action):
		# action(up:0, down:1, left:2, right:3)
		original_pos = self.pos.copy()
		out_of_boundary = False
		if action == self.actions.up:
			if self.pos[0] - 1 >= 0:
				self.pos[0] = self.pos[0] - 1
			else:
				out_of_boundary = True
		elif action == self.actions.down:
			if self.pos[0] + 1 < self.height:
				self.pos[0] = self.pos[0] + 1
			else:
				out_of_boundary = True
		elif action == self.actions.left:
			if self.pos[1] - 1 >= 0:
				self.pos[1] = self.pos[1] - 1
			else:
				out_of_boundary = True
		elif action == self.actions.right:
			if self.pos[1] + 1 < self.width:
				self.pos[1] = self.pos[1] + 1
			else:
				out_of_boundary = True

		if (self.pos[0], self.pos[1]) == self.goal:
			reward = 1
			self.done = True
		elif self.grid[self.pos[0], self.pos[1]] == -1:
			reward = 0
			self.pos = original_pos
		elif out_of_boundary:
			reward = 0
			self.pos = original_pos
		else:
			reward = 0
			self.grid[self.pos[0], self.pos[1]] = 1
			self.grid[original_pos[0], original_pos[1]] = 0

		return self.grid.copy(), reward, self.done

	def set_agent_pos(self, row, col):
		assert row < self.height
		assert col < self.width

		original_pos = self.pos.copy()
		self.grid[original_pos[0], self.original_pos[1]] = 0
		self.pos = [row, col]
		self.grid[self.pos[0], self.pos[1]] = 1

		return self.grid.copy()

	def load_file(self, file):
		with open(file, 'r') as f:
			grid_map = f.readlines()
		grid_map_array = np.array(
			list(map(
				lambda x: list(map(
					lambda y: int(y),
					x.split(' ')
				)),
				grid_map
			))
		)

		self.grid = grid_map_array
		self.height = grid_map_array.shape[0]
		self.width = grid_map_array.shape[0]
		agent_pos = np.argwhere(grid_map_array == 1)
		goal_pos = np.argwhere(grid_map_array == 2)
		assert agent_pos.shape[0] == 1 and goal_pos.shape[0] == 1
		self.pos = [agent_pos[0][0], agent_pos[0][1]]
		self.goal = (goal_pos[0][0], goal_pos[0][1])
		print(grid_map_array, self.height, self.width)

	def render(self):
		return self.grid.copy()



if __name__ == '__main__':
	env = GridWorld()
	state = env.reset(random_loc=False)
	state = env.step(1)
	env.step(1)
	env.step(1)
	env.step(1)
	env.step(2)
	env.step(2)
	env.step(1)
	state = env.step(2)
	state = env.reset(random_loc=False)
	
	print(state)