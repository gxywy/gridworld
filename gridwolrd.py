from argparse import Action
import numpy as np
from enum import IntEnum

class GridWorld:

	def __init__(self, size=(5, 5)):
		assert len(size) == 2, "input x and y"
		assert size[0] > 0 and size[1] > 0, "input positive number"

		self.height = size[0]
		self.width = size[1]
		self.size = size
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

	def reset(self, random_agent=False):
		'''
			observation: agent: 1
						 goal: 2
						 wall: -1
						 else: 0
		'''
		self.grid = np.zeros(self.grid.shape)
		
		if random_agent is True:
			# random agent position
			random_pos = np.random.randint(self.height * self.width - 1)
			self.pos = [random_pos // self.height, random_pos % self.width]
		else:
			self.pos = [0, 0]

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

		if (self.pos[0], self.pos[1]) == self.goal:			# 到达目标
			reward = 1
			self.done = True
		elif self.grid[(self.pos[0], self.pos[1])] == -1:		# 撞墙
			reward = 0
			self.pos = original_pos
		elif out_of_boundary:				# 越界
			reward = 0
			self.pos = original_pos
		else:								# 正常
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
		pass
	
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