# -*- coding: utf-8 -*-
"""
Created on Thu Mar 07 17:24:34 2019

@author: sxd170431
"""

import random
from copy import deepcopy

class Block():

    def __init__(self,number):
        self.block_number = number
        self.clear = False
        self.table = False

    def set_clear(self):
        self.clear = True
        
    def set_onTable(self):
        self.table = True

    def __repr__(self):
        return "b"+self.block_number

class Tower():

    def __init__(self,number):
        self.tower_number = number
        self.block_stack = [Block(self.tower_number+str(i)) for i in range(1)]
        top_block = Block(self.tower_number+str(len(self.block_stack)+1))
        top_block.set_clear()
        bottom_block = self.block_stack[0]
        bottom_block.set_onTable()
        self.block_stack.append(top_block)
        
    def remove_blocks(self):
        self.block_stack = []

    def pop_block(self):
        top_block = self.get_top_block()
        top_block.set_onTable()
        self.block_stack = self.block_stack[:-1]
        N = len(self.block_stack)
        if N:
            self.block_stack[N-1].set_clear()
            
    def add_block(self,block):
        self.block_stack.append(block)

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
          "onTable(+state,+block)",
          "clear(+state,+block)",
          "height(+state,+tower,#h)",
          "putDown(state,tower,block)",
          "stack(state,tower,block)"]

    def __init__(self,number=1,start=False):
        if start:
            self.state_number = number
            self.towers = [Tower(str(i+1)) for i in range(2)]
            self.all_actions = []
            
    def valid(self,action):
        
        pred = action[0]
        tower = action[1]
        block = action[2]
        if pred == "putDown":
            if not block.clear:
                return False
            if block.table:
                return False
            if tower.tower_number != str(block.block_number)[0]:
                return False
        if pred == "stack":
            if tower.tower_number == str(block.block_number)[0]:
                return False
            if not block.clear:
                return False
        return True

    def get_all_actions(self):
        self.all_actions = []
        for action in ["putDown","stack"]:
            blocks = []
            for tower in self.towers:
                for block in tower.get_blocks():
                    blocks.append(block)
            for tower in self.towers:
                for block in blocks:
                    if self.valid((action,tower,block)):
                        self.all_actions.append((action,tower,block))
        
    
    def add_tower(self,tower):
        self.towers.append(tower)

    def goal(self):
        #print "length of towers", len(self.towers)
        for tower in self.towers:
            if tower.too_high():
                #print ("goal checking single block",tower.block_stack)
                #raw_input()
                return False
            #print ("goal checking greater than 1 block", tower.block_stack)
        return True

    def print_world(self):
        for tower in self.towers:
            print (tower)
            

    def execute_action(self,action):
        
        self.state_number += 1
        pred = action[0]
        tower = action[1]
        block = action[2]
        tower_blocks = tower.get_blocks()
        no_of_blocks = len(tower_blocks)
        last_but_one_block_index = no_of_blocks-2 #because indexing starts at 0
        last_but_one_block = tower_blocks[last_but_one_block_index]
        if pred == "putDown":
            if not block.clear:
                return self
            if block.table:
                return self
            if tower.tower_number != str(block.block_number)[:-1]:
                return self
            no_of_towers = len(self.towers)
            max_tower_number = max([int(t5.tower_number) for t5 in self.towers])
            new_tower_id = max_tower_number + 1
            new_tower = Tower(str(new_tower_id))
            new_tower.remove_blocks()
            block.set_onTable()
            block.block_number = new_tower.tower_number+str(0)
            new_tower.add_block(block)
            self.add_tower(new_tower)
            last_but_one_block.set_clear()
            tower.pop_block()
        elif pred == "stack":
            block_tower_number = 0
            if not block.clear:
                return self
            if tower.tower_number == str(block.block_number)[:-1]:
                return self
            if block.table:
                block_tower_number = str(block.block_number)[:-1]
            #tower_to_pop_off = 't'+str(block.block_number)[0]
            for t in self.towers:
                if t.tower_number == str(block.block_number)[:-1]:
                    t.pop_block()
            prev_top_block = tower.get_top_block()
            prev_top_block.clear = False
            block.block_number = tower.tower_number+str(no_of_blocks+1)
            tower.add_block(block)
            if block.table:
                for t2 in self.towers:
                    if t2.tower_number == block_tower_number:
                        self.towers.remove(t2)
                block.table = False
        return self

    def get_state_facts(self):
        facts = []
        for tower in self.towers:
            blocks = tower.get_blocks()
            n_blocks = len(blocks)
            last_block_in_tower = tower.get_top_block()
            for i in range(n_blocks-1):
                if blocks[i].clear:
                    facts.append("clear(s"+str(self.state_number)+",b"+blocks[i].block_number+")")
                if blocks[i].table:
                    facts.append("onTable(s"+str(self.state_number)+",b"+blocks[i].block_number+")")
                facts.append("on(s"+str(self.state_number)+",t"+tower.tower_number+",b"+blocks[i].block_number+",b"+blocks[i+1].block_number+")")
            facts.append("clear(s"+str(self.state_number)+",b"+last_block_in_tower.block_number+")")
            if n_blocks == 1:
               facts.append("onTable(s"+str(self.state_number)+",b"+last_block_in_tower.block_number+")") 
            
        '''
        for tower in self.towers:
            blocks = tower.get_blocks()
            n_blocks = len(blocks)
            if n_blocks == 1:
                only_block = blocks[0]
                facts.append("onTable(s"+str(self.state_number)+",b"+only_block.block_number+")")
            for i in range(n_blocks-1):
                #block i+1 is on block i on(S,A,B) means B is on A in stat S
                if i == 0:
                    facts.append("onTable(s"+str(self.state_number)+",b"+blocks[i].block_number+")")
                facts.append("on(s"+str(self.state_number)+",t"+tower.tower_number+",b"+blocks[i].block_number+",b"+blocks[i+1].block_number+")")
            for i in range(n_blocks):
                if blocks[i].table:
                    facts.append("onTable(s"+str(self.state_number)+",b"+blocks[i].block_number+")")
        '''
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
            sampled_action_predicate = sampled_action[0]
            #sampled_action_string = sampled_action_predicate+"(s"+str(self.state_number)+","+str(sampled_action[2])+")"
            sampled_action_string = sampled_action_predicate+"(s"+str(self.state_number)+","+str(sampled_action[1])+","+str(sampled_action[2])+")."
            #sampled_action_string = "putDown(s"+str(self.state_number)+","+str(sampled_action[0])+","+str(sampled_action[1])+")."
            #print (self.get_state_facts())
            #print (sampled_action_string)
            new_state = self.execute_action(sampled_action)
            #print (new_state.get_state_facts())
            #print ("state_number incremented when executing action: ",new_state.state_number)
            #print ("new_state facts",new_state.get_state_facts())
            actions_not_executed = [action for action in self.all_actions if action != sampled_action]
            return (new_state, [sampled_action_string], actions_not_executed)
        else:
            for tower in self.towers:
                if tower.too_high():
                    block = tower.get_top_block()
                    action = ("putDown",tower,block)
                    action_string = "putDown(s"+str(self.state_number)+","+str(action[1])+","+str(action[2])+")."
                    new_state = self.execute_action(action)
                    actions_not_executed = [item for item in self.all_actions if item != action]
                    return (new_state, [action_string], actions_not_executed)
            '''
            N = len(self.all_actions)
            action_potentials = [1 for i in range(N)]
            action_probabilities = [potential/float(sum(action_potentials)) for potential in action_potentials]
            probability_distribution_function = zip(self.all_actions, action_probabilities)
            sampled_action = self.sample(probability_distribution_function)
            sampled_action_predicate = sampled_action[0]
            sampled_action_string = sampled_action_predicate+"(s"+str(self.state_number)+","+str(sampled_action[1])+","+str(sampled_action[2])+")."
            new_state = self.execute_action(sampled_action)
            actions_not_executed = [action for action in self.all_actions if action != sampled_action]
            return (new_state, [sampled_action_string], actions_not_executed)
            '''
                    

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
