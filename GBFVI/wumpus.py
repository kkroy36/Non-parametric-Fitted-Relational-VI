import random
from copy import deepcopy
class Wumpus(object):
    '''represents the 2D wumpus world'''

    bk = ["stench(+state)",
          "breeze(+state)",
          "gold(+state)",
          "adj(+state,-state)",
          "adj(-state,+state)",
          "right(state)",
          "top(state)",
          "down(state)",
          "left(state)"]

    def __init__(self,N=4,number=1,start=False):
        '''class constructor'''
        if start:
            self.size = N
            self.state_number = number
            self.grid = [[0 for i in range(N)] for j in range(N)]
            self.goal_x,self.goal_y = self.size-1,self.size-1
            self.all_actions = ["left","right","top","down"]
            self.grid[2][1] = 1 #wumpus
            self.grid[2][0] = -1 #pit
            self.position = (0,0)
            self.prev_state = None

    def goal(self):
        if self.position == (self.goal_x,self.goal_y):
            return True
        return False

    def valid(self,x,y):
        '''checks if (x,y) is a valid position'''
        if x < 0 or x == self.size or y < 0 or y == self.size:
            return False
        return True

    def execute_action(self,action):
        '''takes an action and returns new state'''
        self.prev_state = deepcopy(self)
        self.state_number += 1
        x,y = self.position[0],self.position[1]
        if action in self.all_actions:
            if action == "left":
                if self.valid(x-1,y) and abs(self.grid[x-1][y]) != 1:
                    self.position = (x-1,y)
                else:
                    self.position = (x,y)
            elif action == "right":
                if self.valid(x+1,y) and abs(self.grid[x+1][y]) != 1:
                    self.position = (x+1,y)
                else:
                    self.position = (x,y)
            elif action == "top":
                if self.valid(x,y+1) and abs(self.grid[x][y+1]) != 1:
                    self.position = (x,y+1)
                else:
                    self.position = (x,y)
            elif action == "down":
                if self.valid(x,y-1) and abs(self.grid[x][y-1]) != 1:
                    self.position = (x,y-1)
                else:
                    self.position = (x,y)
        else:
            self.position = (x,y)
        return self

    def get_state_facts(self):
        facts = []
        if self.prev_state == None:
            facts = ["start(s"+str(self.state_number)+")"]
        else:
            if self.prev_state.position == self.position:
                return self.prev_state.get_state_facts()
            else:
                facts = ["adj(s"+str(self.prev_state.state_number)+",s"+str(self.state_number)+")"]
        valid = self.valid
        x,y = self.position[0],self.position[1]
        if x == self.goal_x and y == self.goal_y:
            facts.append("gold(s"+str(self.state_number)+")")
        if valid(x-1,y):
            if self.grid[x-1][y] == 1:
                facts.append("stench(s"+str(self.state_number)+")")
            if self.grid[x-1][y] == -1:
                facts.append("breeze(s"+str(self.state_number)+")")
        if valid(x+1,y):
            if self.grid[x+1][y] == 1:
                facts.append("stench(s"+str(self.state_number)+")")
            if self.grid[x+1][y] == -1:
                facts.append("breeze(s"+str(self.state_number)+")")
        if valid(x,y+1):
            if self.grid[x][y+1] == 1:
                facts.append("stench(s"+str(self.state_number)+")")
            if self.grid[x][y+1] == -1:
                facts.append("breeze(s"+str(self.state_number)+")")
        if valid(x,y-1):
            if self.grid[x][y-1] == 1:
                facts.append("stench(s"+str(self.state_number)+")")
            if self.grid[x][y-1] == -1:
                facts.append("breeze(s"+str(self.state_number)+")")
        return facts

    def sample(self,pdf):
        cdf = [(i, sum(p for j,p in pdf if j < i)) for i,_ in pdf]
        R = max(i for r in [random.random()] for i,c in cdf if c <= r)
        return R

    def execute_random_action(self,N=4):

        if random.random() > 1:
            #self.get_all_actions()
            #random_actions = []
            #action_potentials = []
            '''
            for i in range(N):
                random_action = choice(self.all_actions)
                random_actions.append(random_action)
                action_potentials.append(randint(1, 9))
            '''
            N = len(self.all_actions)
            action_potentials = [1 for i in range(N)]
            action_probabilities = [potential/float(sum(action_potentials)) for potential in action_potentials]
            probability_distribution_function = zip(self.all_actions, action_probabilities)
            sampled_action = self.sample(probability_distribution_function)
            sampled_action_string = sampled_action+"(s"+str(self.state_number)+")."
            new_state = self.execute_action(sampled_action)
            actions_not_executed = [action for action in self.all_actions if action != sampled_action]
            return (new_state, [sampled_action_string], actions_not_executed)

        else:
            facts = self.get_state_facts()
            if (("stench" not in fact for fact in facts) and ("breeze" not in fact for fact in facts)):
                current_position = self.position
                new_state = self.execute_action("top")
                if new_state.position != current_position:
                    sampled_action_string = "top"+"(s"+str(self.state_number)+")."
                    actions_not_executed = [action for action in self.all_actions if action != "top"]
                    return (new_state, [sampled_action_string], actions_not_executed)
                else:
                    new_state = self.execute_action("right")
                    if new_state.position != current_position:
                        sampled_action_string = "right"+"(s"+str(self.state_number)+")."
                        actions_not_executed = [action for action in self.all_actions if action != "right"]
                        return (new_state, [sampled_action_string], actions_not_executed)
                    else:
                        N = len(self.all_actions)
                        action_potentials = [1 for i in range(N)]
                        action_probabilities = [potential/float(sum(action_potentials)) for potential in action_potentials]
                        probability_distribution_function = zip(self.all_actions, action_probabilities)
                        sampled_action = self.sample(probability_distribution_function)
                        sampled_action_string = sampled_action+"(s"+str(self.state_number)+")."
                        new_state = self.execute_action(sampled_action)
                        actions_not_executed = [action for action in self.all_actions if action != sampled_action]
                        return (new_state, [sampled_action_string], actions_not_executed)
            else:
                N = len(self.all_actions)
                action_potentials = [1 for i in range(N)]
                action_probabilities = [potential/float(sum(action_potentials)) for potential in action_potentials]
                probability_distribution_function = zip(self.all_actions, action_probabilities)
                sampled_action = self.sample(probability_distribution_function)
                sampled_action_string = sampled_action+"(s"+str(self.state_number)+")."
                new_state = self.execute_action(sampled_action)
                actions_not_executed = [action for action in self.all_actions if action != sampled_action]
                return (new_state, [sampled_action_string], actions_not_executed)
                        
    '''
    def factored(self,state):
        #returns a factored state of
           x,y,I(stench),I(breeze)
        #
        x,y = state[0],state[1]
        if not self.valid(x,y):
            print "In valid grid cell"
            exit()
        state = [x]+[y]
        state += [1 if "stench" in self.obsMap[x][y] else 0]
        state += [1 if "breeze" in self.obsMap[x][y] else 0]
        return state

    def __repr__(self):
        #defines the representation of the grid
           that will be output on call to print
        #
        string = "Wumpus map: \n"
        for i in range(self.size):
            for j in range(self.size):
                string += [str(self.grid[i][j])+", " if j!=self.size-1 else str(self.grid[i][j])+"\n"][0]
        string += "\nObservation map: \n"
        for i in range(self.size):
            for j in range(self.size):
                string += [str(self.obsMap[i][j])+", " if j!=self.size-1 else str(self.obsMap[i][j])+"\n"][0]
        return string+"\nGoal Position: ("+str(self.goal_x)+","+str(self.goal_y)+")"+"\n"
    '''
'''
with open("wumpus_out.txt","a") as f:
    i = 0
    while i < 2:
        state = Wumpus(start=True)
        f.write("start state: "+str(state.get_state_facts())+"\n")
        while not state.goal():
            f.write("="*80+"\n")
            state_action_pair = state.execute_random_action()
            state = state_action_pair[0]
            f.write(str(state.get_state_facts())+"\n")
        i += 1
'''
