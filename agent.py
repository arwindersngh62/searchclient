from state import State
from frontier import FrontierBFS, FrontierDFS, FrontierBestFirst
from heuristic import HeuristicAStar, HeuristicWeightedAStar, HeuristicGreedy
from graphsearch import search
from enum import Enum
from collections import deque


    

class Agent:
    def __init__(self,name,coords,color:'Color'):
        self.name = name
        self.coords = coords
        self.pre_coords = coords
        self.color = color
        self.is_assigned = False
        self.agent_path = []
        self.box_path = []
        self.plans = []

    def reset_agent(self):
        self.is_assigned =False
        self.agent_path = []
        self.box_path = []

    def add_paths(self,paths):
        self.agent_path = paths[0]
        self.box_path = paths[1]
