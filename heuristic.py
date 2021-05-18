from abc import ABCMeta, abstractmethod

class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        pass
    
    def h(self, state: 'State') -> 'int':
        raise NotImplementedError
    
    @abstractmethod
    def f(self, state: 'State') -> 'int': pass
    
    @abstractmethod
    def __repr__(self): raise NotImplementedError

class HeuristicAStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.h(state)
    
    def __repr__(self):
        return 'A* evaluation'

class HeuristicWeightedAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)
    
    def __repr__(self):
        return 'WA*({}) evaluation'.format(self.w)

class HeuristicGreedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def h(self,state):
        for row in range(len(state.goals)):
            for col in range(len(state.goals[row])):
                goal = state.goals[row][col]   
                if 'A' <= goal <= 'Z':
                    goal_cords = (row,col)
                    break
                elif '0' <= goal <= '9':
                    goal_cords =  (row,col)
                    break
        
        for row in range(len(state.boxes)):
            for col in range(len(state.boxes[row])):
                box = state.boxes[row][col]
                if not (box=='\0'):
                    box_cords = (row,col)
                    break
                else:
                    box_cords = ()
        dist = abs(goal_cords[0]-state.agent_rows[0])+abs(goal_cords[1]-state.agent_cols[0])
        if box_cords:        
            dist_box = abs(box_cords[0]-goal_cords[0])+abs(box_cords[1]-goal_cords[1])
            dist = min(dist,dist_box)
        return(dist)
    
    def f(self, state: 'State') -> 'int':
        return self.h(state)
    
    def __repr__(self):
        return 'greedy evaluation'
