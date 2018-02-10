from box_world import Logistics
from time import clock
from GradientBoosting import GradientBoosting

class FVI(object):

    def __init__(self,burn_in_time=2,simulator="logistics"):
        self.burn_in_time = burn_in_time
        self.simulator = simulator

    def compute_value_of_trajectory(self,trajectory,discount_factor = 0.9,goal_value = 10): 
        reversed_trajectory = trajectory[::-1]
        number_of_transitions = len(reversed_trajectory)
        values = {}
        for i in range(number_of_transitions):
            state_number = reversed_trajectory[i][0]
            state = reversed_trajectory[i][1]
            value_of_state = (goal_value)*(discount_factor**i) #immediate reward 0
            key = (state_number,tuple(state))
            values[key] = value_of_state
        return values
            
    def compute_burn_in_values(self):
        facts,examples,bk = [],[],[]
        i = 0
        burn_in_facts = []
        burn_in_examples = []
        while i < self.burn_in_time:
            print (i)
            if self.simulator == "logistics":
                state = Logistics(start=True)
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
                print ("goal satisfied")
                values = self.compute_value_of_trajectory(trajectory)
                for key in values:
                    facts += list(key[1])
                    #print (key[1])
                    example_predicate = "value(s"+str(key[0])+") "+str(values[key])
                    examples.append(example_predicate)
                    #print (example_predicate)
                i += 1
        reg = GradientBoosting(regression = True,treeDepth=3)
        reg.setTargets(["value"])
        reg.learn(facts,examples,bk)
        reg.infer(facts,examples)

f = FVI()
f.compute_burn_in_values()
            
