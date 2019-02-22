import random
from copy import deepcopy

class Block():

    def __init__(self,number):
        self.block_number = number
        self.clear = False

    def set_clear(self):
        self.clear = True

    def __repr__(self):
        return "b"+self.block_number

class Tower():

    def __init__(self,number):
        self.tower_number = number
        self.block_stack = [Block(self.tower_number+str(i)) for i in range(random.randint(1,2))]
        top_block = Block(self.tower_number+str(len(self.block_stack)+1))
        top_block.set_clear()
        self.block_stack.append(top_block)

    def pop_block(self):
        self.block_stack = self.block_stack[:-1]
        N = len(self.block_stack)
        if N:
            self.block_stack[N-1].set_clear()

    def get_blocks(self):
        return self.block_stack

    def get_top_block(self):
        N = len(self.block_stack)
        return self.block_stack[N-1]

    def contains(self,block):
        for b in self.block_stack:
            if block.block_number == b.block_number:
                return True
        return False

    def too_high(self):
        if len(self.block_stack) > 1:
            return True
        return False

    def __repr__(self):
        return "t"+str(self.tower_number)
    
class Blocks_world():

    bk = ["on(+state,+tower,+block,-block)",
          "on(+state,+tower,-block,+block)",
          "putDown(state,tower,block)"]

    def __init__(self,number=1,start=False):
        if start:
            self.state_number = number
            self.towers = [Tower(str(i+1)) for i in range(random.randint(1,3))]
            self.all_actions = []

    def get_all_actions(self):
        self.all_actions = []
        for tower in self.towers:
            for block in tower.get_blocks():
                self.all_actions.append((tower,block))

    def goal(self):
        for tower in self.towers:
            if tower.too_high():
                return False
        return True

    def print_world(self):
        for tower in self.towers:
            print (tower)

    def execute_action(self,action):
        
        self.state_number += 1
        tower = action[0]
        block = action[1]
        if tower.contains(block):
            if block.clear:
                tower.pop_block()
            elif not block.clear:
                return self
        return self

    def get_state_facts(self):
        facts = []
        for tower in self.towers:
            blocks = tower.get_blocks()
            n_blocks = len(blocks)
            for i in range(n_blocks-1):
                #block i+1 is on block i on(S,A,B) means B is on A in stat S
                facts.append("on(s"+str(self.state_number)+",t"+tower.tower_number+",b"+blocks[i].block_number+",b"+blocks[i+1].block_number+")")
        return facts

    def sample(self,pdf):
        cdf = [(i, sum(p for j,p in pdf if j < i)) for i,_ in pdf]
        R = max(i for r in [random.random()] for i,c in cdf if c <= r)
        return R

    def execute_random_action(self,actn_dist=0.5):
        self.get_all_actions()
        if random.random() > actn_dist:
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
            sampled_action_string = "putDown(s"+str(self.state_number)+","+str(sampled_action[0])+","+str(sampled_action[1])+")."
            new_state = self.execute_action(sampled_action)
            #print ("state_number incremented when executing action: ",new_state.state_number)
            #print ("new_state facts",new_state.get_state_facts())
            actions_not_executed = [action for action in self.all_actions if action != sampled_action]
            return (new_state, [sampled_action_string], actions_not_executed)
        else:
            for tower in self.towers:
                if tower.too_high():
                    block = tower.get_top_block()
                    action = (tower,block)
                    action_string = "putDown(s"+str(self.state_number)+","+str(action[0])+","+str(action[1])+")."
                    new_state = self.execute_action(action)
                    #print ("state_number incremented when executing action: ",new_state.state_number)
                    #print ("new_state facts",new_state.get_state_facts())
                    actions_not_executed = [item for item in self.all_actions if item != action]
                    return (new_state, [action_string], actions_not_executed)
                else:
                    N = len(self.all_actions)
                    action_potentials = [1 for i in range(N)]
                    action_probabilities = [potential/float(sum(action_potentials)) for potential in action_potentials]
                    probability_distribution_function = zip(self.all_actions, action_probabilities)
                    sampled_action = self.sample(probability_distribution_function)
                    sampled_action_string = "putDown(s"+str(self.state_number)+","+str(sampled_action[0])+","+str(sampled_action[1])+")."
                    new_state = self.execute_action(sampled_action)
                    #print ("state_number incremented when executing action: ",new_state.state_number)
                    #print ("new_state facts",new_state.get_state_facts())
                    actions_not_executed = [action for action in self.all_actions if action != sampled_action]
                    return (new_state, [sampled_action_string], actions_not_executed)
                    

'''
with open("blocks_world_out.txt","a") as f:
    i = 0
    while i < 2:
        state = Blocks_world(start=True)
        state.print_world()
        f.write("start state: "+str(state.get_state_facts())+"\n")
        while not state.goal():
            f.write("="*80+"\n")
            state_action_pair = state.execute_random_action()
            state = state_action_pair[0]
            f.write(str(state.get_state_facts())+"\n")
        i += 1
'''
