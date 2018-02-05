from box_world import Logistics
class FVI(object):

    def __init__(self,burn_in_time=1,simulator="logistics"):
        self.burn_in_time = burn_in_time
        if simulator == "logistics":
            self.start_state = self.logistics_start()

    def logistics_start(self):
        return Logistics(start=True)

    def compute_burn_in_values(self):
        for i in range(self.burn_in_time):
            state = self.start_state
            print (state)
            while not state.goal():
                state = state.execute_random_action()
                for city in state.cities:
                    print ("city info: ",city,city.get_trucks(),city.unloaded_boxes)
                    for truck in city.get_trucks():
                        print ("truck info: ",city,truck,truck.get_boxes())
                        for box in truck.get_boxes():
                            print ("box info: ",box,truck,city)
                #raw_input()

f = FVI()
f.compute_burn_in_values()
            
