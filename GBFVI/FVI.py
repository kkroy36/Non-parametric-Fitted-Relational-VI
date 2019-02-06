from box_world import Logistics
import os
#from wumpus import Wumpus
#from blocks import Blocks_world
#from blackjack import Game
#from chain import Chain
#from net_admin import Admin
# from pong import Pong #--> uncomment to run Pong
# from tetris import Tetris #--> uncomment to run Tetris
from time import clock
from copy import deepcopy
from GradientBoosting import GradientBoosting
path="C://Users//sxd170431//Desktop//Work//Projects//Relational_RL//Results//"

class FVI(object):
    
    def __init__(self, transfer=0, simulator="logistics", batch_size=10, number_of_iterations=50, loss="LS", trees=10,path=path,runs=5, policy=0.9,run_latest=0,test_trajectory_length=50):
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
        self.current_run=run_latest
        self.test_trajectory_no=test_trajectory_length
        """These are the statistics that needs to be averaged accross runs"""
        self.bellman_error=[]
        
        """These contain true and infered Q(s,a) values for every state action pair in the test trajectory"""
        self.true_state_action_val=[]
        self.inf_state_action_val=[]
        self.test_error_state_action=[]
        
        """These contain true and infered Q(s,a) values for just the first state action pair in the test trajectory"""
        self.true_start_state_action_val=[]
        self.inf_start_state_action_val=[]
        self.test_start_error_state_action=[]
        
        """This is the path where results for a particular run would be stored"""
        self.resultpath=path+self.simulator+"//Runs_"+str(runs)+"//Policy_"+str(policy)+"//trees_"+str(self.trees)+"//"+self.loss+"//"
        
        self.compute_transfer_model()
                

    def compute_value_of_trajectory(self, values, trajectory, discount_factor=0.99, goal_value=1.0, AVI=False):
        '''computes the value of a trajectory
           by value iteration until convergence
        '''
        reversed_trajectory = trajectory[::-1]
        number_of_transitions = len(reversed_trajectory)
        immediate_reward = -1
        if not AVI:  # if not AVI i.e. for first iteration perform value iteration for initial values
            # while True:
            #old_values = deepcopy(values)
            for i in range(number_of_transitions):
                if i == 0:
                    next_state_value = goal_value
                    current_state_number = reversed_trajectory[i][0]
                    current_state = reversed_trajectory[i][1][:-1]
                    current_action = reversed_trajectory[i][1][-1]
                    value_of_state = immediate_reward + discount_factor * next_state_value  # V(S) = R(S) + gamma*goal_value
                    key = (current_state_number, tuple(current_state[:-1]))
                    values[current_action][key] = value_of_state
                else:
                    next_state_number = reversed_trajectory[i-1][0]
                    next_state = reversed_trajectory[i-1][1][:-1]
                    next_state_action = reversed_trajectory[i-1][1][-1]
                    next_state_value = values[next_state_action][(next_state_number, tuple(next_state[:-1]))]
                    current_state_number = reversed_trajectory[i][0]
                    current_state = reversed_trajectory[i][1][:-1]
                    current_action = reversed_trajectory[i][1][-1]
                    value_of_state = immediate_reward + discount_factor*next_state_value #V(S) = R(S) + gamma*V(S')
                    key = (current_state_number, tuple(current_state[:-1]))
                    values[current_action][key] = value_of_state
            
        elif AVI:  # perform value iteration by infering value of next state for value iteration from fiitted model
            for i in range(number_of_transitions-1):
                state_number = trajectory[i][0]
                state = trajectory[i][1][:-1]
                state_action = trajectory[i][1][-1]
                next_state_number = trajectory[i+1][0]
                next_state = trajectory[i+1][1][:-1]
                next_state_action = trajectory[i+1][1][-1]
                #print 'current_state,current_action.next_state,next_state_action',state,state_action,next_state,next_state_action
                facts = list(next_state)
                examples = [next_state_action+" "+str(0.0)]
                value_of_next_state = 0.0
                try:
                    self.model.infer(facts, examples)
                    value_of_next_state = self.model.testExamples[next_state_action.split('(')[0]][next_state_action]
                except:
                    value_of_next_state = 0.0
                value_of_state = immediate_reward + discount_factor * value_of_next_state  # V(S) = R(S) + gamma*V_hat(S')
                key = (state_number, tuple(state[:-1]))
                values[state_action][key] = value_of_state
                
    def compute_value_of_test_trajectory(self, values, trajectory, discount_factor=0.99, goal_value=1.0, AVI=False):
        '''computes the value of a trajectory
           by value iteration until convergence
        '''
        reversed_trajectory = trajectory[::-1]
        number_of_transitions = len(reversed_trajectory)
        immediate_reward = -1
        
        """Calculate the original Q-values from Bellman backup equation"""
        for i in range(number_of_transitions):
            if i == 0:
                next_state_value = goal_value
                current_state_number = reversed_trajectory[i][0]
                current_state = reversed_trajectory[i][1][:-1]
                current_action = reversed_trajectory[i][1][-1]
                value_of_state = immediate_reward + discount_factor * next_state_value  # V(S) = R(S) + gamma*goal_value
                key = (current_state_number, tuple(current_state[:-1]))
                #print 'current_action,state',current_action,key
                values[current_action][key] = value_of_state
            else:
                next_state_number = reversed_trajectory[i-1][0]
                next_state = reversed_trajectory[i-1][1][:-1]
                next_state_action = reversed_trajectory[i-1][1][-1]
                next_state_value = values[next_state_action][(next_state_number, tuple(next_state[:-1]))]
                current_state_number = reversed_trajectory[i][0]
                current_state = reversed_trajectory[i][1][:-1]
                current_action = reversed_trajectory[i][1][-1]
                value_of_state = immediate_reward + discount_factor*next_state_value #V(S) = R(S) + gamma*V(S')
                key = (current_state_number, tuple(current_state[:-1]))
                #print 'current_action,state',current_action,key
                values[current_action][key] = value_of_state
        #print "Length of trajectory", len(trajectory)
        #raw_input()
        """Calculate the infered Q-values from the Fitted Value Iteration model, also calculate the error"""                                 
     
        for i in range(number_of_transitions-1):
            state_number = trajectory[i][0]
            state = trajectory[i][1][:-1]
            state_action = trajectory[i][1][-1]
            next_state_number = trajectory[i+1][0]
            next_state = trajectory[i+1][1][:-1]
            next_state_action = trajectory[i+1][1][-1]
            #print 'current_state,current_action.next_state,next_state_action',state,state_action,next_state,next_state_action
            facts = list(next_state)
            examples = [next_state_action+" "+str(0.0)]
            value_of_next_state = 0.0
            try:
                self.model.infer(facts, examples)
                value_of_next_state = self.model.testExamples[next_state_action.split('(')[0]][next_state_action]
            except:
                value_of_next_state = 0.0
            infered_state_value = immediate_reward + discount_factor * value_of_next_state  # V(S) = R(S) + gamma*V_hat(S')
            key = (state_number, tuple(state[:-1]))
            #print 'current_action,state,next_state_action,next_state',state,state_action, next_state,next_state_action
            #raw_input()
            true_state_value=values[state_action][key]
            
            """Q(s,a) for all state action pairs in the test trajectory"""
            self.true_state_action_val.append(true_state_value)
            self.inf_state_action_val.append(infered_state_value)
            self.test_error_state_action.append(abs(infered_state_value - true_state_value))
            
            """Q(s,a) for the first state action pair in the test trajectory"""
            if (i==0):
               
               print "The value of i is",i 
               self.true_start_state_action_val.append(true_state_value)
               self.inf_start_state_action_val.append(infered_state_value)
               self.test_start_error_state_action.append(abs(infered_state_value - true_state_value))
               with open(self.resultpath+"testing_error_start.txt","a") as fp:
                    fp.write(str(abs(infered_state_value - true_state_value))+"\n")
               with open(self.resultpath+"true_values_start.txt","a") as fp:
                    fp.write(str(true_state_value)+"\n")
               with open(self.resultpath+"inferred_values_start.txt","a") as fp:
                    fp.write(str(infered_state_value)+"\n") 
            
            with open(self.resultpath+"testing_error.txt","a") as fp:
                fp.write(str(abs(infered_state_value - true_state_value))+"\n")
            with open(self.resultpath+"true_values.txt","a") as fp:
                fp.write(str(true_state_value)+"\n")
            with open(self.resultpath+"inferred_values.txt","a") as fp:
                fp.write(str(infered_state_value)+"\n")
        
    def get_targets(self, examples):
        '''returns the targets'''
        return list(set([item.split('(')[0] for item in examples]))

    def init_values(self, values, trajectory):
        '''initializes 2D values dictionary
           with an entry for each grounded target (action)
        '''
        for item in trajectory:
            key = item[1][-1]
            print "key is", key
            if key not in values:
                values[key] = {}

    def compute_transfer_model(self):
        '''computes the transfer model if transfer=1
           therefore it computes transfer model over 6 iterations
           if set to 1, which can be changed in the code
           otherwise, it uses at least one trajectory to compute the initial model
           before starting fitted value iteration.
           Note that in the transfer start state, parameters to allow different grid sizes,
           lets say for wumpus world can be set during object call if allowable by the constructor.
        '''
        
        """Creates separate run directories in the destination folder to store results from each run"""
        dirName=self.resultpath+"//Run"+str(self.current_run)
        if not os.path.exists(self.resultpath+"//Run"+str(self.current_run)):
           os.makedirs(dirName)
           print("Directory " , dirName ,  " Created ")
        else:    
           print("Directory " , dirName ,  " already exists")   
        
        self.resultpath=dirName+"//"
        
        facts, examples, bk, reward_function = [], [], [], []
        i = 0
        values = {}
        while i < 5:  # at least ten iteration burn in time
            if self.simulator == "logistics":
                state = Logistics(number=self.state_number, start=True)
                if not bk:
                    bk = Logistics.bk
            elif self.simulator == "pong":
                state = Pong(number=self.state_number, start=True)
                if not bk:
                    bk = Pong.bk
            elif self.simulator == "tetris":
                state = Tetris(number=self.state_number, start=True)
                if not bk:
                    bk = Tetris.bk
            elif self.simulator == "wumpus":
                state = Wumpus(number=self.state_number, start=True)
                if not bk:
                    bk = Wumpus.bk
            elif self.simulator == "blocks":
                state = Blocks_world(number=self.state_number, start=True)
                if not bk:
                    bk = Blocks_world.bk
            elif self.simulator == "blackjack":
                state = Game(number=self.state_number, start=True)
                if not bk:
                    bk = Game.bk
            elif self.simulator == "50chain":
                state = Chain(number=self.state_number, start=True)
                if not bk:
                    bk = Chain.bk
            elif self.simulator == "net_admin":
                state = Admin(number=self.state_number, start=True)
                if not bk:
                    bk = Admin.bk
            with open(self.simulator+"_transfer_out.txt", "a") as f:
                if self.transfer:
                    f.write("start state: "+str(state.get_state_facts())+"\n")
                time_elapsed = 0
                within_time = True
                start = clock()
                trajectory = []
                while not state.goal():
                    if self.transfer:
                        f.write("="*80+"\n")
                    s_number = state.state_number
                    s_facts = state.get_state_facts()
                    state_action_pair = state.execute_random_action()
                    state = state_action_pair[0]  # state
                    # action and remove period
                    action = state_action_pair[1][0][:-1]
                    if self.transfer:
                        f.write(str(state.get_state_facts())+"\n")
                    trajectory.append((s_number, s_facts+[action]))
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
                    #print "The trajectory is",trajectory
                    self.init_values(values, trajectory)
                    self.compute_value_of_trajectory(values, trajectory)
                    self.state_number += len(trajectory)+1
                    for target in values:
                        for state in values[target]:
                            facts += tuple(state[1])
                            examples.append(
                                target+" "+str(values[target][state]))
                    i += 1
        targets = self.get_targets(examples)
        reg = GradientBoosting(regression=True, treeDepth=3,
                               trees=self.trees, loss=self.loss)
        reg.setTargets(targets)
        reg.learn(facts, examples, bk)
        self.model = reg
        self.AVI()
        if self.transfer:
            self.AVI()

    def compute_bellman_error(self, trajectories):
        '''computes max bellman error for every iteration'''
        bellman_errors = []
        immediate_reward = -1
        discount_factor = 0.99
        for trajectory in trajectories:
            number_of_transitions = len(trajectory)
            for i in range(number_of_transitions-1):
                state_number = trajectory[i][0]
                state = trajectory[i][1][:-1]
                state_action = trajectory[i][1][-1]
                next_state_number = trajectory[i+1][0]
                next_state = trajectory[i+1][1][:-1]
                next_state_action = trajectory[i+1][1][-1]
                #print 'current_state,current_action.next_state,next_state_action',state,state_action,next_state,next_state_action
                facts = list(next_state)
                examples = [next_state_action+" "+str(0.0)]
                value_of_next_state = 0.0
                value_of_current_state = 0.0
                try:
                    self.model.infer(list(state),[state_action+" "+str(0.0)])
                    value_of_current_state = self.model.testExamples[state_action.split('(')[0]][state_action]
                except:
                    value_of_current_state = 0.0
                try:
                    self.model.infer(facts, examples)
                    value_of_next_state = self.model.testExamples[next_state_action.split('(')[0]][next_state_action]
                except:
                    value_of_next_state = 0.0
                bellman_error = abs((immediate_reward + discount_factor * value_of_next_state) - value_of_current_state)  # |R(S) + gamma*V_hat(S') - V_hat(S)|
                bellman_errors.append(bellman_error)
        return (sum(bellman_errors)/float(len(bellman_errors))) #return average or max, right now average
        

    def AVI(self):
        #values = {}
        for i in range(self.number_of_iterations):
            trajectories = []
            j = 0
            facts, examples, bk = [], [], []
            values = {}
            while j < self.batch_size:
                if self.simulator == "logistics":
                    state = Logistics(number=self.state_number, start=True)
                    if not bk:
                        bk = Logistics.bk
                elif self.simulator == "pong":
                    state = Pong(number=self.state_number, start=True)
                    if not bk:
                        bk = Pong.bk
                elif self.simulator == "tetris":
                    state = Tetris(number=self.state_number, start=True)
                    if not bk:
                        bk = Tetris.bk
                elif self.simulator == "wumpus":
                    state = Wumpus(number=self.state_number, start=True)
                    if not bk:
                        bk = Wumpus.bk
                elif self.simulator == "blocks":
                    state = Blocks_world(number=self.state_number, start=True)
                    if not bk:
                        bk = Blocks_world.bk
                elif self.simulator == "blackjack":
                    state = Game(number=self.state_number, start=True)
                    if not bk:
                        bk = Game.bk
                elif self.simulator == "50chain":
                    state = Chain(number=self.state_number, start=True)
                    if not bk:
                        bk = Chain.bk
                elif self.simulator == "net_admin":
                    state = Admin(number=self.state_number, start=True)
                    if not bk:
                        bk = Admin.bk
                with open(self.resultpath+self.simulator+"_FVI_out.txt", "a") as fp:
                    fp.write("*"*80+"\nstart state: " +
                             str(state.get_state_facts())+"\n")
                    time_elapsed = 0
                    within_time = True
                    start = clock()
                    trajectory = []
                    while not state.goal():
                        fp.write("="*80+"\n")
                        s_number = state.state_number
                        s_facts = state.get_state_facts()
                        state_action_pair = state.execute_random_action()
                        state = state_action_pair[0]  # state
                        # action and remove period
                        action = state_action_pair[1][0][:-1]
                        fp.write(str(state.get_state_facts())+"\n")
                        trajectory.append((s_number, s_facts+[action]))
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
                    #print "The  trajectory is", trajectory
                    trajectories.append(trajectory)
                    if within_time:
                        self.init_values(values, trajectory)
                        if i == 0:
                            self.compute_value_of_trajectory(
                                values, trajectory, AVI=True)
                        else:
                            # perform computation using fitted value iteration
                            self.compute_value_of_trajectory(
                                values, trajectory, AVI=True)
                        self.state_number += 1
                        print "The value function is", values
                        for key in values:
                            if values[key]:
                                examples_string = key
                                for state_key in values[key]:
                                    facts += list(state_key[1])
                                    examples_string += " " + \
                                        str(values[key][state_key])
                                examples.append(examples_string)
                        j += 1
            # self.model.infer(facts,examples)
            fitted_values = self.model.infer(facts, examples)
            bellman_error = self.compute_bellman_error(trajectories)
            self.bellman_error.append(bellman_error)
            with open(self.resultpath+self.simulator+"_BEs.txt", "a") as f:
                f.write("iteration: "+str(i) +
                        " average bellman error: "+str(bellman_error)+"\n")
            examples = []
            for key in values:  # TODO fix this
                if values[key]:
                    examples_string = key
                    for state_key in values[key]:
                        examples_string += " "+str(values[key][state_key])
                    examples.append(examples_string)
            targets = self.get_targets(examples)
            self.model.setTargets(targets)
            self.model.learn(facts, examples, bk)
        i = 0 
        while i < self.test_trajectory_no: #test trajectories for logistics
            if self.simulator == "logistics": # Add other domains specific to testing
                state = Logistics(number=self.state_number, start=True)
                time_elapsed = 0
                within_time = True
                start = clock()
                trajectory = []
                while not state.goal():
                    s_number = state.state_number
                    s_facts = state.get_state_facts()
                    state_action_pair = state.execute_random_action()
                    state = state_action_pair[0]
                    action = state_action_pair[1][0][:-1]
                    trajectory.append((s_number, s_facts+[action]))
                    end = clock()
                    time_elapsed = abs(end-start)
                    if self.simulator == "logistics" and time_elapsed > 1:
                        within_time = False
                        i=i-1
                        break
                if within_time:
                    #print "************* i is", i
                    #print "The  test trajectory is", trajectory 
                    #raw_input()
                    self.init_values(values, trajectory)
                    self.compute_value_of_test_trajectory(values, trajectory, AVI=True)
                    self.state_number += 1
            i += 1
