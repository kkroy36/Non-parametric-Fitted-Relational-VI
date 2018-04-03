from box_world import Logistics
from wumpus import Wumpus
from blocks import Blocks_world
from blackjack import Game
from chain import Chain
from net_admin import Admin
#from pong import Pong #--> uncomment to run Pong
from tetris import Tetris #--> uncomment to run Tetris
from time import clock
from GradientBoosting import GradientBoosting

class FVI(object):

    def __init__(self,transfer=0,simulator="logistics",batch_size=1,number_of_iterations=10,loss="LS",trees=10):
	'''transfer = 1, means a prespecified number of iterations are run and learning
	   the regression model using RFGB, (relational model) before starting fitted
           value iteration with the learned values
	'''
        self.transfer = transfer
        self.simulator = simulator
        self.batch_size = batch_size
        self.loss = loss
        self.trees = trees
        self.number_of_iterations = number_of_iterations
        self.model = None
	self.state_number = 1
        self.compute_transfer_model()

    def compute_value_of_trajectory(self,values,trajectory,discount_factor=0.97,goal_value=10,AVI=False):
	'''computes the value of a trajectory
           if trajectory from AVI=True, then gather next state value from prediciton
           else gather it from the discounted number of steps from the goal times the goal reward
           there is only one trajectory, therefore, R + gamma*expected(next_state_value) becomes
           R + gamma*next_state_value
	   hence this was carried out as shown in the code
           reason for not averaging (expected value) is because everytime the objects are different
           Hence, it may appear to be a TD update, but it is not.
	''' 
        reversed_trajectory = trajectory[::-1]
        number_of_transitions = len(reversed_trajectory)
        if not AVI:
            for i in range(number_of_transitions):
                state_number = reversed_trajectory[i][0]
                state = reversed_trajectory[i][1]
                value_of_state = (goal_value)*(discount_factor**i) #immediate reward 0
                key = (state_number,tuple(state))
                values[key] = value_of_state
        elif AVI:
            for i in range(number_of_transitions-1):
                state_number = trajectory[i][0]
                state = trajectory[i][1]
                next_state_number = trajectory[i+1][0]
                next_state = trajectory[i+1][1]
                facts = list(next_state)
                examples = ["value(s"+str(next_state_number)+") "+str(0.0)]
                self.model.infer(facts,examples)
                value_of_next_state = self.model.testExamples["value"]["value(s"+str(next_state_number)+")"]
                value_of_state = discount_factor*value_of_next_state
                key = (state_number,tuple(state))
                values[key] = value_of_state
                
            
    def compute_transfer_model(self):
	'''computes the transfer model if transfer=1
           therefore it computes transfer model over 6 iterations
           if set to 1, which can be changed in the code
	   otherwise, it uses at least one trajectory to compute the initial model
           before starting fitted value iteration.
	   Note that in the transfer start state, parameters to allow different grid sizes,
	   lets say for wumpus world can be set during object call if allowable by the constructor.
	'''
        facts,examples,bk = [],[],[]
        i = 0
        values = {}
        while i < 1: #at least one iteration burn in time
            if self.simulator == "logistics":
                state = Logistics(number=self.state_number,start=True)
                if not bk:
                    bk = Logistics.bk
		    print (Logistics.reward_function)
		    exit()
            elif self.simulator == "pong":
                state = Pong(number=self.state_number,start=True)
                if not bk:
                    bk = Pong.bk
            elif self.simulator == "tetris":
                state = Tetris(number=self.state_number,start=True)
                if not bk:
                    bk = Tetris.bk
            elif self.simulator == "wumpus":
                state = Wumpus(number=self.state_number,start=True)
                if not bk:
                    bk = Wumpus.bk
            elif self.simulator == "blocks":
                state = Blocks_world(number=self.state_number,start=True)
                if not bk:
                    bk = Blocks_world.bk
            elif self.simulator == "blackjack":
                state = Game(number=self.state_number,start=True)
                if not bk:
                    bk = Game.bk
            elif self.simulator == "50chain":
                state = Chain(number=self.state_number,start=True)
                if not bk:
                    bk = Chain.bk
            elif self.simulator == "net_admin":
                state = Admin(number=self.state_number,start=True)
                if not bk:
                    bk = Admin.bk
            with open(self.simulator+"_transfer_out.txt","a") as f:
                if self.transfer:
                    f.write("start state: "+str(state.get_state_facts())+"\n")
                time_elapsed = 0
                within_time = True
                start = clock()
                trajectory = [(state.state_number,state.get_state_facts())]
                while not state.goal():
                    if self.transfer:
                        f.write("="*80+"\n")
                    state_action_pair = state.execute_random_action()
                    state = state_action_pair[0] #state
                    if self.transfer:
                        f.write(str(state.get_state_facts())+"\n")
                    trajectory.append((state.state_number,state.get_state_facts()))
                    end = clock()
                    time_elapsed = abs(end-start)
                    if self.simulator == "logistics" and time_elapsed > 0.5:
                        within_time = False
                        break
                    elif self.simulator == "pong" and time_elapsed > 1000:
                        within_time = False
                        break
                    elif self.simulator == "tetris" and time_elapsed > 1000:
                        within_time = False
                        break
                    elif self.simulator == "wumpus" and time_elapsed > 1:
                        within_time = False
                        break
                    elif self.simulator == "blocks" and time_elapsed > 1:
                        within_time = False
                        break
                    elif self.simulator == "blackjack" and time_elapsed > 1:
                        within_time = False
                        break
                    elif self.simulator == "50chain" and time_elapsed > 1:
                        within_time = False
                        break
                    elif self.simulator == "net_admin" and time_elapsed > 1:
                        within_time = False
                        break
                if within_time:
                    self.compute_value_of_trajectory(values,trajectory)
		    self.state_number += len(trajectory)+1
                    for key in values:
                        facts += list(key[1])
                        example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                        examples.append(example_predicate)
                    i += 1
        reg = GradientBoosting(regression = True,treeDepth=2,trees=self.trees,loss=self.loss)
        reg.setTargets(["value"])
        reg.learn(facts,examples,bk)
        self.model = reg
        self.AVI()
	if self.transfer:
	    self.AVI()

    def compute_bellman_error(self,values):
        bellman_errors = []
        inferred_values = self.model.testExamples["value"]
        for key in values:
            predicate = "value(s"+str(key[0])+")"
            inferred_value = inferred_values[predicate]
            computed_value = values[key]
            bellman_error = computed_value - inferred_value 
            bellman_errors.append(abs(bellman_error))
            values[key] = inferred_value + bellman_error
        #return max(bellman_errors)
        return sum(bellman_errors)/float(len(bellman_errors)) #average bellman error

    def AVI(self):
        for i in range(self.number_of_iterations):
            j = 0
            facts,examples,bk = [],[],[]
            values = {}
            while j < self.batch_size:
                if self.simulator == "logistics":
                    state = Logistics(number=self.state_number,start=True)
                    if not bk:
                        bk = Logistics.bk
                elif self.simulator == "pong":
                    state = Pong(number=self.state_number,start=True)
                    if not bk:
                        bk = Pong.bk
                elif self.simulator == "tetris":
                    state = Tetris(number=self.state_number,start=True)
                    if not bk:
                        bk = Tetris.bk
                elif self.simulator == "wumpus":
                    state = Wumpus(number=self.state_number,start=True)
                    if not bk:
                        bk = Wumpus.bk
                elif self.simulator == "blocks":
                    state = Blocks_world(number=self.state_number,start=True)
                    if not bk:
                        bk = Blocks_world.bk
                elif self.simulator == "blackjack":
                    state = Game(number=self.state_number,start=True)
                    if not bk:
                        bk = Game.bk
                elif self.simulator == "50chain":
                    state = Chain(number=self.state_number,start=True)
                    if not bk:
                        bk = Chain.bk
                elif self.simulator == "net_admin":
                    state = Admin(number=self.state_number,start=True)
                    if not bk:
                        bk = Admin.bk
                with open(self.simulator+"_FVI_out.txt","a") as fp:
                    fp.write("*"*80+"\nstart state: "+str(state.get_state_facts())+"\n")
                    time_elapsed = 0
                    within_time = True
                    start = clock()
                    trajectory = [(state.state_number,state.get_state_facts())]
                    while not state.goal():
                        fp.write("="*80+"\n")
                        state_action_pair = state.execute_random_action()
                        state = state_action_pair[0]
                        fp.write(str(state.get_state_facts())+"\n")
                        trajectory.append((state.state_number,state.get_state_facts()))
                        end = clock()
                        time_elapsed = abs(end-start)
                        if self.simulator == "logistics" and time_elapsed > 0.5:
                            within_time = False
                            break
                        elif self.simulator == "pong" and time_elapsed > 1000:
                            within_time = False
                            break
                        elif self.simulator == "tetris" and time_elapsed > 10:
                            within_time = False
                            break
                        elif self.simulator == "wumpus" and time_elapsed > 1:
                            within_time = False
                            break
                        elif self.simulator == "blocks" and time_elapsed > 1:
                            within_time = False
                            break
                        elif self.simulator == "blackjack" and time_elapsed > 1:
                            within_time = False
                            break
                        elif self.simulator == "50chain" and time_elapsed > 1:
                            within_time = False
                            break
                        elif self.simulator == "net_id" and time_elapsed > 1:
                            within_time = False
                    if within_time:
                        self.compute_value_of_trajectory(values,trajectory)
			self.state_number += 1
                        for key in values:
                            facts += list(key[1])
                            example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                            examples.append(example_predicate)
                        j += 1
            #self.model.infer(facts,examples)
            fitted_values = self.model.infer(facts,examples)
            bellman_error = self.compute_bellman_error(values)
            with open(self.simulator+"_BEs.txt","a") as f:
                f.write("iteration: "+str(i)+" average bellman error: "+str(bellman_error)+"\n")
            examples = []
            for key in values:
                example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                examples.append(example_predicate)
            self.model.learn(facts,examples,bk)
