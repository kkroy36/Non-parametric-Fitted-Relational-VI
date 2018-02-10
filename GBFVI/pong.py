#PONG pygame

import random
import pygame, sys
from pygame.locals import *
from pykeyboard import PyKeyboard
#from random import randint,choice,random
from time import clock
#from pyautogui import typewrite


pygame.init()

fps = pygame.time.Clock()
#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

p1_hit = False
p2_hit = False
p1_inline = False
p2_inline = False
p1_close = False
p2_close = False

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    horz = random.randrange(2+8,4+8)
    vert = random.randrange(1+8,3+8)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT/2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT/2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score,p1_hit,p2_hit,p1_inline,p2_inline,p1_close,p2_close
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    if int(ball_pos[1]) in range(paddle1_pos[1] - 3*HALF_PAD_HEIGHT,paddle1_pos[1] + 3*HALF_PAD_HEIGHT,1):
        p1_inline = True

    if int(ball_pos[1]) in range(paddle2_pos[1] - 3*HALF_PAD_HEIGHT,paddle2_pos[1] + 3*HALF_PAD_HEIGHT,1):
        p2_inline = True

    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]):
        p1_close = True

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        p2_close = True
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        p1_hit = True
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        p2_hit = True
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))  
    
    
#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_i:
        paddle2_vel = -8
    elif event.key == K_k:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_i, K_k):
        paddle2_vel = 0

init()

def send_key(key):
    '''simulates key press'''
    keyboard = PyKeyboard()
    keyboard.press_key(key)
    keyboard.release_key(key)

'''   
while True:
    draw(window)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps.tick(60)
'''

class Pong(object):
    '''class to represent the Pong world'''

    bk = ["inline(+state,+player)",
          "close(+state,+player)",
          "value(state)"]

    @staticmethod
    def initialize():
        init()

    def __init__(self,number=1,start=False):
        '''class constructor'''
        global p1_hit,p2_hit,p1_inline,p2_inline,p1_close,p2_close
        self.all_actions = ['w','s','i','k']
        p1_hit,p2_hit,p1_inline,p2_inline,p1_close,p2_close = False,False,False,False,False,False
        if start:
            Pong.initialize()
            self.state_number = number
            self.p1_hit = p1_hit
            self.p2_hit = p2_hit
            self.p1_close = p1_close
            self.p2_close = p2_close
            self.p1_inline = p1_inline
            self.p2_inline = p2_inline
            self.paddle1_pos_x = paddle1_pos[0]
            self.paddle1_pos_y = paddle1_pos[1]
            self.paddle2_pos_x = paddle2_pos[0]
            self.paddle2_pos_y = paddle2_pos[1]
            self.ball_pos_x = ball_pos[0]
            self.ball_pos_y = ball_pos[1]
            self.score = l_score
            self.opponent_score = r_score
        #self.start = self
        #self.features = ["paddle1_xpos","paddle1_ypos","paddle2_xpos","paddle2_ypos","ball_xpos","ball_ypos","score","opponent_score"]

    def goal(self):
        if self.p1_hit or self.p2_hit:
            return True
        return False
    
    def execute_action(self,action):
        '''returns new state
           invalid action does nothing
        '''
        self.state_number += 1
        global paddle1_pos,paddle2_pos,ball_pos,l_score,r_score,p1_hit,p2_hit,p1_inline,p2_inline,p1_close,p2_close
        if action not in self.all_actions:
            return self
        paddle1_pos = [self.paddle1_pos_x,self.paddle1_pos_y]
        paddle2_pos = [self.paddle2_pos_x,self.paddle2_pos_y]
        ball_pos = [self.ball_pos_x,self.ball_pos_y]
        l_score = self.score
        r_score = self.opponent_score
        i = 0
        while i < 10:
            draw(window)
            for event in pygame.event.get():
                send_key(action)
                if event.type == KEYDOWN:
                    keydown(event)
                elif event.type == KEYUP:
                    keyup(event)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            fps.tick(60)
            i += 1
        self.p1_hit = p1_hit
        self.p2_hit = p2_hit
        self.p1_inline = p1_inline
        self.p2_inline = p2_inline
        self.p1_close = p1_close
        self.p2_close = p2_close
        p1_hit,p2_hit,p1_inline,p2_inline,p1_close,p2_close = False,False,False,False,False,False
        self.paddle1_pos_x = paddle1_pos[0]
        self.paddle1_pos_y = paddle1_pos[1]
        self.paddle2_pos_x = paddle2_pos[0]
        self.paddle2_pos_y = paddle2_pos[1]
        self.ball_pos_x = ball_pos[0]
        self.ball_pos_y = ball_pos[1]
        self.score = l_score
        self.opponent_score = r_score
        return self

    def get_state_facts(self):
        facts = []
        if self.p1_hit:
            facts += ["close(s"+str(self.state_number)+",p1)"]
            facts += ["inline(s"+str(self.state_number)+",p1)"]
        elif not self.p1_hit:
            if self.p1_inline:
                facts += ["inline(s"+str(self.state_number)+",p1)"]
            elif self.p1_close:
                facts += ["close(s"+str(self.state_number)+",p1)"]
        if self.p2_hit:
            facts += ["close(s"+str(self.state_number)+",p2)"]
            facts += ["inline(s"+str(self.state_number)+",p2)"]
        elif not self.p2_hit:
            if self.p2_inline:
                facts += ["inline(s"+str(self.state_number)+",p2)"]
            elif self.p2_close:
                facts += ["close(s"+str(self.state_number)+",p2)"]
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
        return (new_state,[random_action],actions_not_executed)

    def factored(self,state):
        '''returns all feature values of the state as a list'''
        factored_state = [state.paddle1_pos_x]
        factored_state += [state.paddle1_pos_y]
        factored_state += [state.paddle2_pos_x]
        factored_state += [state.paddle2_pos_y]
        factored_state += [state.ball_pos_x]
        factored_state += [state.ball_pos_y]
        factored_state += [state.score]
        factored_state += [state.opponent_score]
	return factored_state

    def __repr__(self):
        '''outputs this on call to print'''
        output_string = "\npaddle1 position: ("+str(self.paddle1_pos_x)+","+str(self.paddle1_pos_y)+")"
        output_string += "\npaddle2 position: ("+str(self.paddle2_pos_x)+","+str(self.paddle2_pos_y)+")"
        output_string += "\nball position: ("+str(self.ball_pos_x)+","+str(self.ball_pos_y)+")" 
        output_string += "your score: "+str(self.score)
        output_string += "opponent score: "+str(self.opponent_score)
        return output_string
'''  
with open("pong_out.txt","a") as f:
    i = 0
    while i < 3:
        state = Pong(start=True)
        f.write("start state: "+str(state.get_state_facts())+"\n")
        while not state.goal():
            f.write("="*80+"\n")
            state_action_pair = state.execute_random_action()
            state = state_action_pair[0]
            f.write(str(state.get_state_facts())+"\n")
        i += 1
'''
