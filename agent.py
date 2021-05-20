from state import State
from frontier import FrontierBFS, FrontierDFS, FrontierBestFirst
from heuristic import HeuristicAStar, HeuristicWeightedAStar, HeuristicGreedy
from graphsearch import search
from enum import Enum
from collections import deque

from itertools import zip_longest

    

class Agent:
    def __init__(self,name,coords,color:'Color'):
        self.name = name
        self.coords = coords
        self.pre_coords = coords
        self.color = color
        self.is_assigned = False
        self.agent_path = []
        self.box_path = []
        self.plan = None
        self.next_plan = None
        self.plan_actions = None
        self.curr_time = 0
        self.final_path = []
        self.actions = []
    
    def has_next_action(self):
        if len(self.actions)>0:
            return True
        return False

    def reset_agent(self):
        self.is_assigned =False
        self.agent_path = []
        self.box_path = []

    def add_paths(self,paths):
        self.agent_path = paths[0]
        self.box_path = paths[1]

    def create_timed_plan(self):
        time_plan = []
        if self.plan.box == None:
            for i in range(len(self.plan.agent_path)):
                time_plan.append((self.plan.agent_path[i],(None,None),i+self.curr_time)) 
                
            self.plan.agent_path = time_plan
        else:
            # for i in range(len(self.plan.agent_path)):
            agent_box_path = list(zip_longest(self.plan.agent_path, self.plan.box_path, fillvalue=(None, None)))
            for i in range(len(agent_box_path)):
                # time_plan.append(, ())
                # print(f'{self.name} : {agent_box_path[i]}')
                time_plan.append((*agent_box_path[i], i+self.curr_time))
                # time_plan.append((self.plan.agent_path[i],self.box_path[i],i+self.curr_time)) 
            self.plan.agent_path = time_plan

    # final_path = ((x,y),(bx,by), s)

    def finalize_curr_plan(self):
        if (self.plan == None):
            print("Plan doesnt exist, finalize_curr_plan")
            return
        self.final_path += self.plan.agent_path
        # print(self.plan.agent_path)
        # print(f" Last one: {self.plan.agent_path[-1]}")
        self.curr_time = self.curr_time + self.plan.agent_path[-1][2] + 1 
        if self.next_plan != None:
            self.coords = self.plan.agent_path[-1]
            self.plan = self.next_plan
            self.next_plan = None
        else:
            self.plan=None
        
        
