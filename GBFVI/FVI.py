from box_world import Logistics
from time import clock
from GradientBoosting import GradientBoosting

class FVI(object):

    def __init__(self,burn_in_time=2,simulator="logistics",batch_size=2,number_of_iterations=5):
        self.burn_in_time = burn_in_time
        self.simulator = simulator
        self.batch_size = batch_size
        self.number_of_iterations = number_of_iterations
        self.model = None
        #self.facts,self.examples,self.bk = [],[],[] 

    def compute_value_of_trajectory(self,values,trajectory,discount_factor=0.9,goal_value=10): 
        reversed_trajectory = trajectory[::-1]
        number_of_transitions = len(reversed_trajectory)
        for i in range(number_of_transitions):
            state_number = reversed_trajectory[i][0]
            state = reversed_trajectory[i][1]
            value_of_state = (goal_value)*(discount_factor**i) #immediate reward 0
            key = (state_number,tuple(state))
            values[key] = value_of_state
            
    def compute_burn_in_values(self):
        facts,examples,bk = [],[],[]
        i = 0
        values = {}
        while i < self.burn_in_time:
            if self.simulator == "logistics":
                state = Logistics(start=True)
                if not bk:
                    bk = Logistics.bk
            print ("start state: ",state.get_state_facts())
            time_elapsed = 0
            start = clock()
            trajectory = [(state.state_number,state.get_state_facts())]
            while not state.goal():
                print "="*80
                state_action_pair = state.execute_random_action()
                state = state_action_pair[0] #state
                trajectory.append((state.state_number,state.get_state_facts()))
                end = clock()
                time_elapsed = abs(end-start)
                if time_elapsed > 0.5:
                    break
            if time_elapsed <= 0.5:
                self.compute_value_of_trajectory(values,trajectory)
                for key in values:
                    facts += list(key[1])
                    example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                    examples.append(example_predicate)
                i += 1
        reg = GradientBoosting(regression = True,treeDepth=2)
        reg.setTargets(["value"])
        reg.learn(facts,examples,bk)
        self.model = reg
        self.AVI()

    def compute_bellman_error(self,values):
        bellman_error = []
        inferred_values = self.model.testExamples["value"]
        for key in values:
            predicate = "value(s"+str(key[0])+")"
            inferred_value = inferred_values[predicate]
            computed_value = values[key]
            bellman_error.append(abs(inferred_value-computed_value))
            values[key] += computed_value-inferred_value
        return sum(bellman_error)/float(len(bellman_error)) #average bellman error

    def AVI(self):
        f = open("result.txt","a")
        for i in range(self.number_of_iterations):
            j = 0
            facts,examples,bk = [],[],[]
            values = {}
            while j < self.batch_size:
                if self.simulator == "logistics":
                    state = Logistics(start=True)
                    if not bk:
                        bk = Logistics.bk
                print ("start state: ",state.get_state_facts())
                time_elapsed = 0
                start = clock()
                trajectory = [(state.state_number,state.get_state_facts())]
                while not state.goal():
                    print "="*80
                    state_action_pair = state.execute_random_action()
                    state = state_action_pair[0]
                    trajectory.append((state.state_number,state.get_state_facts()))
                    end = clock()
                    time_elapsed = abs(end-start)
                    if time_elapsed > 0.5:
                        break
                if time_elapsed <= 0.5:
                    self.compute_value_of_trajectory(values,trajectory)
                    for key in values:
                        facts += list(key[1])
                        example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                        examples.append(example_predicate)
                    j += 1
            self.model.infer(facts,examples)
            fitted_values = self.model.infer(facts,examples)
            bellman_error = self.compute_bellman_error(values)
            f.write("iteration: "+str(i)+" average bellman error: "+str(bellman_error)+"\n")
            examples = []
            for key in values:
                example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                examples.append(example_predicate)
            self.model.learn(facts,examples,bk)

f = FVI()
f.compute_burn_in_values()
            
