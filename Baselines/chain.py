from math import exp
import random
class Chain(object):
    '''class to represent the 50-chain'''

    bk = ["poor(+state)",
          "low(+state)",
          "high(+state)",
          "excellent(+state)",
          "value(state)"]
    
    def __init__(self,number=1,start=False):
        '''class constructor'''
        if start:
            self.state_number = number
            self.chain = [0 for i in range(50)]
            self.chain[13],self.chain[38] = 1,1
            self.all_actions = ["left","right"]
            self.position = random.randint(0,49)
        #self.features = ["kernel1dens","kernel2dens"]

    def goldPositions(self):
        '''returns the gold positions on the chain'''
        return [13,38]

    def goal(self):
        if self.position == 13 or self.position == 38:
            return True
        return False

    def valid(self,position):
        '''check if chain cell is valid'''
        cell = position
        if cell < 0 or cell > 49:
            return False
        return True

    def execute_action(self,action):
        '''returns new state
           invalid action does nothing
        '''
        self.state_number += 1
        cell = self.position
        if self.goal():
            return self
        if action not in self.all_actions:
            return self
        elif action in self.all_actions:
            if action == "left":
                if self.valid(cell-1):
                    self.position = cell-1
                    return self
                elif not self.valid(cell-1):
                    return self
            elif action == "right":
                if self.valid(cell+1):
                    self.position = cell+1
                    return self
                elif not self.valid(cell+1):
                    return self

    def get_state_facts(self):
        facts = []
        kernels = self.goldPositions()
        Z = 0
        potentials = []
        cell = self.position
        for kernel in kernels:
            potential = self.kernelProb(cell,kernel,2)
            potentials += [potential]
        for potential in potentials:
            if potential >= 0.6:
                facts.append(4)
            if potential >= 0.1 and potential < 0.6:
                facts.append(3)
            if potential >= 0.01 and potential < 0.1:
                facts.append(2)
            elif potential < 0.01:
                facts.append(1)
	return facts

    def sample(self,pdf):
        cdf = [(i, sum(p for j,p in pdf if j < i)) for i,_ in pdf]
        R = max(i for r in [random.random()] for i,c in cdf if c <= r)
        return R

    def execute_random_action(self):
        N = len(self.all_actions)
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

    def kernelProb(self,cell,kernel,std):
        '''gaussian kernel'''
        distance = (cell-kernel)**2
        factor = exp((-0.5*distance)/float(std**2))
        return factor

    def factored(self,cell):
        '''returns probabilities of RBF kernels'''
        kernels = self.goldPositions()
        Z = 0
        factoredCell = []
        for kernel in kernels: 
            prob = self.kernelProb(cell,kernel,4)
            factoredCell += [prob]
            Z += prob
        factoredCell = [prob/float(Z) for prob in factoredCell]
        return factoredCell

    def __repr__(self):
        '''printing the chain
           will output this content
        '''
        return "gold positions: "+" ".join([str(i) for i in self.goldPositions()])+"\n"
'''
with open("chain_out.txt","a") as f:
    i = 0
    while i < 1:
        state = Chain(start=True)
        f.write("start state: "+str(state.get_state_facts())+"\n")
        while not state.goal():
            f.write("="*80+"\n")
            state_action_pair = state.execute_random_action()
            state = state_action_pair[0]
            action = state_action_pair[1]
            f.write(str(state.get_state_facts())+"\n")
            f.write(str(state.position)+"\n")
            f.write(str(action)+"\n")
        i += 1
'''
