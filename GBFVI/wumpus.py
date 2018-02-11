import random
class Wumpus(object):
    '''represents the 2D wumpus world'''

    bk = ["stench(+state)",
          "breeze(+state)",
          "gold(+state)",
          "value(state)"]

    def __init__(self,N=4,number=1,start=False):
        '''class constructor'''
        if start:
            self.size = N
            self.state_number = number
            self.grid = [[0 for i in range(N)] for j in range(N)]
            self.goal_x,self.goal_y = self.size-1,self.size-1
            self.all_actions = ["left","right","top","down"]
            self.grid[2][1] = 1 #wumpus
            self.grid[3][1] = -1 #pit
            self.position = (0,0)

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
