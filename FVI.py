from box_world import Logistics
from time import clock

class FVI(object):

    def __init__(self,burn_in_time=10,simulator="logistics"):
        self.burn_in_time = burn_in_time
        if simulator == "logistics":
            self.start_state = Logistics(start=True)

    def compute_burn_in_values(self):
        i = 0
        while i < self.burn_in_time:
            print (i)
            state = Logistics(start=True)
            print ("start state: ",state)
            time_elapsed = 0
            start = clock()
            while not state.goal():
                state = state.execute_random_action()
                for city in state.cities:
                    print ("city info: ",city,city.get_trucks(),city.unloaded_boxes)
                    for truck in city.get_trucks():
                        print ("truck info: ",city,truck,truck.get_boxes())
                        for box in truck.get_boxes():
                            print ("box info: ",box,truck,city)
                end = clock()
                time_elapsed = abs(end-start)
                if time_elapsed > 0.5:
                    break
            if time_elapsed <= 0.5:
                print ("goal satisfied")
                i += 1

f = FVI()
f.compute_burn_in_values()
            
