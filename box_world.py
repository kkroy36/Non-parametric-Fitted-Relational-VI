from random import randint,choice
from copy import deepcopy

#implicitly all cities assumed interconnected

class City(object):

    MAX_CITIES = 3

    def __init__(self,number):
        self.trucks = []
        self.city_number = number
        self.unloaded_boxes = []

    def get_truck(self,truck_number):
        for truck in self.get_trucks():
            if truck.get_number() == truck_number:
                return truck
        return False

    def remove_truck(self,truck_to_remove):
        print ("city: ",str(self))
        print ("removing truck: ",truck_to_remove)
        self.trucks = [truck for truck in self.trucks if str(truck)!=str(truck_to_remove)]
        print ("trucks after removing: ",self.trucks)

    def get_trucks(self):
        return self.trucks

    def get_number(self):
        return self.city_number

    def get_unloaded_box(self,box_number):
        for box in self.unloaded_boxes:
            if box.get_number() == box_number:
                return box
        return False

    def remove_unloaded_box(self,b):
        self.unloaded_boxes = [box for box in self.unloaded_boxes if str(box)!=str(b)]

    def add_truck(self,truck):
        print ("city: ",str(self))
        print ("adding truck: ",truck)
        print ("right before adding: ",self.trucks)
        truck.change_location(self)
        if str(truck) not in [str(s) for s in self.trucks]:
            self.trucks += [truck]
            print ("trucks after appending: ",self.trucks)

    def add_unloaded_box(self,box):
        self.unloaded_boxes.append(box)

    def __repr__(self):
        return "c"+str(self.city_number)

class Box(object):

    def __init__(self,number,truck=False):
        self.location = City(1) #starts at source city
        self.box_number = number
        self.truck = truck
        if truck:
            self.city = self.get_truck().get_location()

    def get_truck(self):
        return self.truck

    def get_number(self):
        return self.box_number

    def get_location(self):
        if self.truck:
            return self.get_truck().get_location()
        return self.location

    def change_truck(self,location):
        self.truck = False
        self.location = location

    def __repr__(self):
        return "b"+str(self.box_number)

class Truck(object):

    def __init__(self,number,city):
        self.boxes = []
        self.MAX_BOXES = 5
        self.location = city #every truck starts at source city
        self.truck_number = number

    def change_location(self,location):
        self.location = location

    def get_location(self):
        return self.location

    def get_number(self):
        return self.truck_number

    def get_boxes(self):
        return self.boxes

    def get_box(self,box_number):
        for box in self.get_boxes():
            if box.get_number() == box_number:
                return box
        return False

    def add_box(self,box):
        self.boxes.append(box)
        box.truck = self

    def remove_box(self,box_to_remove):
        self.boxes = [box for box in self.boxes if str(box)!=str(box_to_remove)]
        box_to_remove.change_truck(self.get_location())
        
    def init_boxes(self,already_existing_trucks,number_of_boxes=False):
        if not number_of_boxes:
            number_of_boxes = randint(1,self.MAX_BOXES)
            
        boxes_already_in_trucks = []
        for truck in already_existing_trucks:
            for box in truck.get_boxes():
                boxes_already_in_trucks.append(str(box))
                
        for i in range(number_of_boxes):
            box = Box(i+1,self)
            if str(box) not in boxes_already_in_trucks:
                self.add_box(box)

    def __repr__(self):
        return "t"+str(self.truck_number)

class Logistics(object): #represents a world state

    def get_move_combinations(self,trucks,cities):
        combinations = []
        for truck in trucks:
            for city in cities:
                combinations.append("move(s"+str(self.state_number)+","+str(truck)+","+str(city)+").")
        return combinations

    def get_load_combinations(self,trucks):
        combinations = []
        for city in self.cities:
            boxes = city.unloaded_boxes
        for truck in trucks:
            for box in boxes:
                combinations.append("load(s"+str(self.state_number)+","+str(box)+","+str(truck)+").")
        return combinations

    def get_unload_combinations(self,trucks):
        combinations = []
        for truck in trucks:
            boxes = truck.get_boxes()
            for box in boxes:
                combinations.append("unload(s"+str(self.state_number)+","+str(box)+","+str(truck)+").")
        return combinations

    def __init__(self,number=1,start=False):
        self.MAX_TRUCKS = 3
        self.state_number = number
        self.cities = None
        self.trucks = None
        self.boxes = None
        if start:
            self.cities = [City(1)] #always start at source city
            self.trucks = self.init_trucks()
        self.all_actions = None

    def goal(self): #at least one box in city 3
        if not self.get_city(3):
            return False
        for city in self.cities:
            if city.get_number() == 3 and len(city.unloaded_boxes) > 0:
                print city.unloaded_boxes
                return True
        return False

    def get_city(self,city_number):
        for city in self.cities:
            if city.get_number() == city_number:
                return city
        return False

    def init_trucks(self,number_of_trucks=False):
        if not number_of_trucks:
            number_of_trucks = randint(1,self.MAX_TRUCKS)
        for i in range(number_of_trucks):
            truck = Truck(i+1,self.cities[0])
            trucks = []
            for city in self.cities:
                trucks = city.get_trucks()
                truck.init_boxes(trucks)
                city.add_truck(truck)

    def get_all_actions(self):
        cities = [City(i+1) for i in range(City.MAX_CITIES)]
        trucks = []
        for city in self.cities:
            for truck in city.get_trucks():
                trucks.append(truck)
        move_combinations = self.get_move_combinations(trucks,cities)
        load_combinations = self.get_load_combinations(trucks)
        unload_combinations = self.get_unload_combinations(trucks)
        self.all_actions = unload_combinations + move_combinations + load_combinations

    def add_city(self,city):
        if str(city) not in [str(c) for c in self.cities]:
            self.cities.append(city)
            print ("new city added")

    def execute_action(self,action):
        print ('='*80)
        print ("action: ",action)
        self.state_number += 1
        action_description = action.split('(')[0]
        if action_description == "move":
            destination_city_number = int(action.split(',')[2][1:-2])
            destination_city = City(destination_city_number)
            move_truck_number = int(action.split(',')[1][1:])
            self.add_city(destination_city)
            for city in self.cities:
                move_truck = city.get_truck(move_truck_number)
                if str(city) == str(destination_city):
                    print ("source and destination same")
                    return self
                if not move_truck:
                    print ("truck in not city")
                    continue
                city.remove_truck(move_truck)
                destination_city.add_truck(move_truck)
                break
        if action_description == "unload":
            unload_truck_number = int(action.split(',')[2][1:-2])
            box_number = int(action.split(',')[1][1:])
            for city in self.cities:
                unload_truck = city.get_truck(unload_truck_number)
                if not unload_truck:
                    print ("truck not among: ",city.get_trucks())
                    continue
                box = unload_truck.get_box(box_number)
                if not box:
                    print ("box not on unload truck: ",truck.get_boxes())
                    return self
                print ("before unloading: ",unload_truck.get_boxes())
                unload_truck.remove_box(box)
                city.add_unloaded_box(box)
                break
        if action_description == "load":
            load_truck_number = int(action.split(',')[2][1:-2])
            box_number = int(action.split(',')[1][1:])
            for city in self.cities:
                trucks = city.get_trucks()
                load_truck = city.get_truck(load_truck_number)
                if not load_truck:
                    continue
                for truck in trucks:
                    if truck.get_box(box_number):
                        return self
                box = city.get_unloaded_box(box_number)
                if not box:
                    return self
                print ("before loading: ",load_truck.get_boxes())
                load_truck.add_box(box)
                city.remove_unloaded_box(box)
                break
        return self

    def execute_random_action(self):
        self.get_all_actions()
        random_action = choice(self.all_actions)
        new_state = self.execute_action(random_action)
        return new_state
        
    def __repr__(self):
        return_string = ""
        city_string = ",".join(str(city) for city in self.cities)
        return_string += "cities: "+city_string+"\n"
        trucks = []
        for city in self.cities:
            trucks += city.get_trucks()
        truck_string = ",".join(str(truck) for truck in trucks)
        return_string += "trucks: "+truck_string+"\n"
        all_boxes = []
        for truck in trucks:
            boxes = truck.get_boxes()
            all_boxes += [str(box) for box in boxes]
        all_boxes = set(all_boxes)
        box_string = ",".join(str(box) for box in all_boxes)
        return_string += "boxes: "+box_string+"\n"
        return return_string

'''
start_state = State(1,start=True)
print (start_state)
for i in range(10):
    print (start_state.execute_random_action())
'''
