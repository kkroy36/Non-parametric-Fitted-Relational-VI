#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import random
from pykeyboard import PyKeyboard
def send_key(key):
    '''simulates key press'''
    keyboard = PyKeyboard()
    keyboard.press_key(key)
    keyboard.release_key(key)
    


# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://hi-im.laria.me/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (me@laria.me)
# or leave a comment on this gist.

# Very simple tetris implementation
# 
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!
# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from random import randrange as rand
import pygame, sys

# The configuration
cell_size =	18
cols =		10
rows =		22
maxfps = 	30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]

def rotate_clockwise(shape):
	return [ [ shape[y][x]
			for y in xrange(len(shape)) ]
		for x in xrange(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[ cy + off_y ][ cx + off_x ]:
					return True
			except IndexError:
				return True
	return False

def remove_row(board, row):
	del board[row]
	return [[0 for i in xrange(cols)]] + board
	
def join_matrixes(mat1, mat2, mat2_off):
	off_x, off_y = mat2_off
	for cy, row in enumerate(mat2):
		for cx, val in enumerate(row):
			mat1[cy+off_y-1	][cx+off_x] += val
	return mat1

def new_board():
	board = [ [ 0 for x in xrange(cols) ]
			for y in xrange(rows) ]
	board += [[ 1 for x in xrange(cols)]]
	return board

class TetrisApp(object):

	def __init__(self):
		pygame.init()
		pygame.key.set_repeat(250,25)
		self.width = cell_size*(cols+6)
		self.height = cell_size*rows
		self.rlim = cell_size*cols
		self.gameover = False
		self.paused = False
		self.n_stones = 0
		self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]
		self.shape_counts = {}
		for shape in tetris_shapes:
                        self.shape_counts[tuple([tuple(item) for item in shape])] = 0
		self.default_font =  pygame.font.Font(
			pygame.font.get_default_font(), 12)
		
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
		                                             # mouse movement
		                                             # events, so we
		                                             # block them.
		self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
		self.init_game()
	
	def new_stone(self):
		self.stone = self.next_stone[:]
		if self.stone in tetris_shapes:
                        stone_tuple = tuple([tuple(item) for item in self.stone])
                        self.shape_counts[stone_tuple] += 1
		self.n_stones += 1
		self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
		self.stone_x = int(cols / 2 - len(self.stone[0])/2)
		self.stone_y = 0
		if check_collision(self.board,
		                   self.stone,
		                   (self.stone_x, self.stone_y)):
			self.gameover = True
	
	def init_game(self):
		self.board = new_board()
		self.new_stone()
		self.level = 1
		self.score = 0
		self.lines = 0
		pygame.time.set_timer(pygame.USEREVENT+1, 1000)
	
	def disp_msg(self, msg, topleft):
		x,y = topleft
		for line in msg.splitlines():
			self.screen.blit(
				self.default_font.render(
					line,
					False,
					(255,255,255),
					(0,0,0)),
				(x,y))
			y+=14
	
	def center_msg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  self.default_font.render(line, False,
				(255,255,255), (0,0,0))
		
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
		
			self.screen.blit(msg_image, (
			  self.width // 2-msgim_center_x,
			  self.height // 2-msgim_center_y+i*22))
	
	def draw_matrix(self, matrix, offset):
		off_x, off_y  = offset
		for y, row in enumerate(matrix):
			for x, val in enumerate(row):
				if val:
					pygame.draw.rect(
						self.screen,
						colors[val],
						pygame.Rect(
							(off_x+x) *
							  cell_size,
							(off_y+y) *
							  cell_size, 
							cell_size,
							cell_size),0)
	
	def add_cl_lines(self, n):
		linescores = [0, 40, 100, 300, 1200]
		self.lines += n
		self.score += linescores[n] * self.level
		if self.lines >= self.level*6:
			self.level += 1
			newdelay = 1000-50*(self.level-1)
			newdelay = 100 if newdelay < 100 else newdelay
			pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
	
	def move(self, delta_x):
		if not self.gameover and not self.paused:
			new_x = self.stone_x + delta_x
			if new_x < 0:
				new_x = 0
			if new_x > cols - len(self.stone[0]):
				new_x = cols - len(self.stone[0])
			if not check_collision(self.board,
			                       self.stone,
			                       (new_x, self.stone_y)):
				self.stone_x = new_x
	def quit(self):
		self.center_msg("Exiting...")
		pygame.display.update()
		sys.exit()
	
	def drop(self, manual):
		if not self.gameover and not self.paused:
			self.score += 1 if manual else 0
			self.stone_y += 1
			if check_collision(self.board,
			                   self.stone,
			                   (self.stone_x, self.stone_y)):
				self.board = join_matrixes(
				  self.board,
				  self.stone,
				  (self.stone_x, self.stone_y))
				self.new_stone()
				cleared_rows = 0
				while True:
					for i, row in enumerate(self.board[:-1]):
						if 0 not in row:
							self.board = remove_row(
							  self.board, i)
							cleared_rows += 1
							break
					else:
						break
				self.add_cl_lines(cleared_rows)
				return True
		return False
	
	def insta_drop(self):
		if not self.gameover and not self.paused:
			while(not self.drop(True)):
				pass
	
	def rotate_stone(self):
		if not self.gameover and not self.paused:
			new_stone = rotate_clockwise(self.stone)
			if not check_collision(self.board,
			                       new_stone,
			                       (self.stone_x, self.stone_y)):
				self.stone = new_stone
	
	def toggle_pause(self):
		self.paused = not self.paused
	
	def start_game(self):
		if self.gameover:
			self.init_game()
			self.gameover = False
	
	def run(self):
		key_actions = {
			'ESCAPE':	self.quit,
			'a':		lambda:self.move(-1),
			'd':	        lambda:self.move(+1),
			's':		lambda:self.drop(True),
			'w':		self.rotate_stone,
			'p':		self.toggle_pause,
			'SPACE':	self.start_game,
			'RETURN':	self.insta_drop
		}
		
		self.gameover = False
		self.paused = False
		
		dont_burn_my_cpu = pygame.time.Clock()
		i = 0
		while 1:
			self.screen.fill((0,0,0))
			if self.gameover:
				self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.score)
			else:
				if self.paused:
					self.center_msg("Paused")
				else:
					pygame.draw.line(self.screen,
						(255,255,255),
						(self.rlim+1, 0),
						(self.rlim+1, self.height-1))
					self.disp_msg("Next:", (
						self.rlim+cell_size,
						2))
					self.disp_msg("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
						(self.rlim+cell_size, cell_size*5))
					self.draw_matrix(self.bground_grid, (0,0))
					self.draw_matrix(self.board, (0,0))
					self.draw_matrix(self.stone,
						(self.stone_x, self.stone_y))
					self.draw_matrix(self.next_stone,
						(cols+1,2))
			pygame.display.update()
			for event in pygame.event.get():
                                #send_key('s')
				if event.type == pygame.USEREVENT+1:
					self.drop(False)
				elif event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.KEYDOWN:
					for key in key_actions:
						if event.key == eval("pygame.K_"
						+key):
							key_actions[key]()
					
			dont_burn_my_cpu.tick(maxfps)
			i += 1

class Tetris(object):
        '''class for Tetris simulator'''

        bk = ["shape_count(+state,+shape,[high;low])",
              "value(state)"]
        
        def __init__(self,number = 1,start=False):
                '''class constructor'''
                if start:
                    self.nstones = 0
                    self.state_number = number
                    self.goal_state = False
                    self.shape_counts = [0 for i in range(7)]
                    self.run = TetrisApp()
                self.all_actions = ['w','a','s','d']

        def goal(self):
            if self.goal_state:
                return True
            return False

        def execute_action(self,action):
                '''returns new state
                   does nothing on invalid actions
                '''
                self.state_number += 1
                if action not in self.all_actions:
                        return state
                key_actions = {
			'ESCAPE':	self.run.quit,
			'a':		lambda:self.run.move(-1),
			'd':	        lambda:self.run.move(+1),
			's':		lambda:self.run.drop(True),
			'w':		self.run.rotate_stone,
			'p':		self.run.toggle_pause,
			'SPACE':	self.run.start_game,
			'RETURN':	self.run.insta_drop
		}
		
		#self.gameover = False
		#self.paused = False
		
		dont_burn_my_cpu = pygame.time.Clock()
                i = 0
		while i < 1:
			self.run.screen.fill((0,0,0))
			if self.run.gameover:
                                self.goal_state = True
                                return self
				#self.run.center_msg("""Game Over!\nYour score: %d Press space to continue""" % self.run.score)
			else:
				if self.run.paused:
					self.run.center_msg("Paused")
				else:
					pygame.draw.line(self.run.screen,
						(255,255,255),
						(self.run.rlim+1, 0),
						(self.run.rlim+1, self.run.height-1))
					self.run.disp_msg("Next:", (
						self.run.rlim+cell_size,
						2))
					self.run.disp_msg("Score: %d\n\nLevel: %d\\nLines: %d" % (self.run.score, self.run.level, self.run.lines),(self.run.rlim+cell_size, cell_size*5))
					self.run.draw_matrix(self.run.bground_grid, (0,0))
					self.run.draw_matrix(self.run.board, (0,0))
					self.run.draw_matrix(self.run.stone,
						(self.run.stone_x, self.run.stone_y))
					self.run.draw_matrix(self.run.next_stone,
						(cols+1,2))
			pygame.display.update()
			for event in pygame.event.get():
                                send_key(action)
				if event.type == pygame.USEREVENT+1:
					self.run.drop(False)
				elif event.type == pygame.QUIT:
					self.run.quit()
				elif event.type == pygame.KEYDOWN:
					for key in key_actions:
						if event.key == eval("pygame.K_"
						+key):
							key_actions[key]()
					
			dont_burn_my_cpu.tick(maxfps)
			i += 1
		self.nstones = self.run.n_stones
		self.shape_counts = self.run.shape_counts.values()
		return self

	def get_state_facts(self):
            facts = []
            facts = [self.nstones]+self.shape_counts
	    '''
            N = len(self.shape_counts)
            for i in range(N):
                if self.shape_counts[i] > 2:
                    facts = [2]
                elif self.shape_counts[i] <=2:
                    facts = [1]
            '''
            return facts

        def sample(self,pdf):
            cdf = [(i, sum(p for j,p in pdf if j < i)) for i,_ in pdf]
            R = max(i for r in [random.random()] for i,c in cdf if c <= r)
            return R

        def execute_random_action(self,N=4):
            random_actions = []
            action_potentials = []
            for i in range(N):
                random_action = random.choice(self.all_actions)
                random_actions.append(random_action)
                action_potentials.append(random.randint(1,9))
            action_probabilities = [potential/float(sum(action_potentials)) for potential in action_potentials]
            actions_not_executed = [action for action in self.all_actions if action != random_action]
            probability_distribution_function = zip(random_actions,action_probabilities)
            sampled_action = self.sample(probability_distribution_function)
            new_state = self.execute_action(sampled_action)
            return (new_state,[sampled_action],actions_not_executed)
            

	def factored(self,state):
                '''returns factored state'''
                return [self.nstones]+self.shape_counts

        def __repr__(self):
                '''outputs this on call to print'''
                output_string = str(self.nstones)+","
                output_string += ",".join([str(x) for x in self.shape_counts])
                return output_string
'''
with open("tetris_out.txt","a") as f:
    i = 0
    while i < 2:
        state = Tetris(start = True)
        f.write("start state: "+str(state.get_state_facts())+"\n")
        while not state.goal():
            f.write("="*80+"\n")
            state_action_pair = state.execute_random_action()
            state = state_action_pair[0]
            f.write(str(state.get_state_facts())+"\n")
        i += 1
'''
