from enum import Enum, unique

@unique
class PlanType(Enum):
    MoveAgent = 0
    MoveBox = 1

class Plan:

    def __init__(self, agent=None,
                       box=None,
                       goal=None,
                       start_time=None,
                       length=None,
                       agent_path=None,
                       box_path=None,
                       next_plan=None):
        self.agent = agent
        self.box = box
        self.goal = goal
        self.length = length
        self.agent_path = agent_path
        self.box_path = box_path
        self.next_plan = next_plan

    def __init__(self, ptype: 'PlanType', goal: 'Coords'):
        self.ptype = ptype
        self.goal = goal

    def add_box(self,box: 'Box'):
        if self.ptype is Plan.MoveAgent:
            pass
        else:
            self.box = box

    
            
                
