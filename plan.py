from enum import Enum, unique

@unique
class PlanType(Enum):
    MoveAgent = 0
    MoveBox = 1

class Plan:
    def __init__(self, ptype: 'PlanType', goal: 'Coords'):
        self.ptype = ptype
        self.goal = goal

    def add_box(self,box: 'Box'):
        if self.ptype is Plan.MoveAgent:
            pass
        else:
            self.box = box

    
            
                
