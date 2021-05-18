from state import State
from frontier import FrontierBFS, FrontierDFS, FrontierBestFirst
from heuristic import HeuristicAStar, HeuristicWeightedAStar, HeuristicGreedy
from graphsearch import search
from enum import Enum
from collections import deque

class TaskType(Enum):
    MoveNextTo = 0
    MoveBox = 1
    MoveTo = 2

class task:
    def __init__(self,type,goal_coords,walls,num_cols,num_rows):
        self.type = type
        self.walls = walls
        self.goal_coords = goal_coords
        self.num_cols = num_cols
        self.num_rows = num_rows
    ## these other attributes are added only in case of box task
    def add_box(self,box):
        self.box = box
    

class Agent:
    def __init__(self,name,coords,color:'Color'):
        self.name = name
        self.coords = coords
        self.pre_coords = coords
        self.color = color
        self.tasks =deque()
        self.curr_task_done=True
        self.plan = []
        self.has_goal = 'N'
        self.agent_path = []
        self.box_path = []

    def add_task(self,task):
        self.tasks.append(task)
    
    def get_next_task(self):
        return self.tasks.popleft()

    def add_replan_task(self):
        self.tasks.appendleft(task)

    def add_move_box(self,goal_coords,walls,num_cols,num_rows,box):
        if self.coords.is_next_to(box.coords):
            print('#Box'+str(box.name)+' is next  to '+str(self.name), flush=True)
            task_t = task(TaskType.MoveBox,goal_coords,walls,num_cols,num_rows)
            task_t.add_box(box)
        else:
            self.tasks.append(task(TaskType.MoveNextTo,box.coords,walls,num_cols,num_rows))
            task_t = task(TaskType.MoveBox,goal_coords,walls,num_cols,num_rows)
            task_t.add_box(box)
        self.add_task(task_t)

    def add_move(self,goal_coords,walls,num_cols,num_rows):
        task_t = task(TaskType.MoveTo,goal_coords,walls,num_cols,num_rows)
        self.add_task(task_t)  


    def solve_current(self):
        print('#Getting tasks the total number of tasks are : '+str(len(self.tasks)), flush=True)
        self.pre_coords=self.coords
        while len(self.tasks)>0:
            task = self.get_next_task()
            if task.type == TaskType.MoveBox:
                print('#moving box'+str(task.box.name)+' from '+str(self.coords.get_coords())+' to goal '+str(task.goal_coords.get_coords()), flush=True)
                plan_t = self.moveBox(task.goal_coords,task.walls,task.num_cols,task.num_rows,task.box.name,task.box.coords)
            #print('#current plan len: '+str(plan_t), flush=True)
            #self.apply_plan(plan_t)
            #print('#current agent coords: '+str(self.coords.get_coords()), flush=True)
                self.plan+=plan_t
            elif task.type == TaskType.MoveNextTo:
                print('#moving next to box'+str(task.goal_coords.get_coords())+'from'+str(self.coords.get_coords()), flush=True)
                plan_t = self.moveTo(task.goal_coords,task.walls,task.num_cols,task.num_rows)
                plan_t = plan_t[0:(len(plan_t)-1)]
            #print('#current plan: '+str(plan_t), flush=True)
                self.apply_plan(plan_t)
            #print('#current agent coords: '+str(self.coords.get_coords()), flush=True)
                self.plan+=plan_t
            elif task.type == TaskType.MoveTo:
                print('#moving to goal'+str(task.goal_coords.get_coords()), flush=True)
                plan_t = self.moveTo(task.goal_coords,task.walls,task.num_cols,task.num_rows)
            #print('#current plan len: '+str(plan_t), flush=True)
            #self.apply_plan(plan_t)
            #print('#current agent coords: '+str(self.coords.get_coords()), flush=True)
                self.plan+=(plan_t)
            self.curr_task =  task
        
    
    def get_current_plan(self):
        return self.plan
            
    def apply_plan(self,plan):
       
        for i in plan:
            #print('#applying plan :'+str(i[0]), flush=True)
            self.coords = self.coords.apply_action(i[0])


    def moveTo(self,goal_coords,walls,num_cols,num_rows):
        path = self.agent_graph_search(goal_coords,walls,'Move',num_cols,num_rows,None,None)
        return (path)

    def moveBox(self,goal_coords,walls,num_cols,num_rows,box_name,box_coords):
        #print('#current agent coords: '+str(goal_coords.get_coords())+' box_coords: '+str(box_coords.get_coords()), flush=True)
        path = self.agent_graph_search(goal_coords,walls,'MoveBox',num_cols,num_rows,box_name,box_coords)
        return (path)

    def agent_graph_search(self,goal_coords,walls,goal_type,num_cols,num_rows,box_name,box_coords):
        if goal_type == 'Move':
            initial_state = self.create_move_state(goal_coords,walls,num_cols,num_rows)
        if goal_type == 'MoveBox':
            #print('#moving box to goal agent coords are'+str(self.coords.get_coords()), flush=True)
            initial_state = self.create_box_state(goal_coords,box_name,box_coords,walls,num_cols,num_rows)
        frontier = FrontierBestFirst(HeuristicGreedy(initial_state))
        plan = search(initial_state, frontier)
        #print('#State :'+str(initial_state.agent_rows)+str(initial_state.agent_cols)+str(initial_state.boxes)+str(initial_state.goals)+str(initial_state.agent_colors)+str(initial_state.box_colors), flush=True)
        #print('#plan :'+str(plan), flush=True)
        return plan

    def create_move_state(self,goal_coords,walls,num_cols,num_rows):
        boxes = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        agent_rows = [self.coords.x]
        agent_cols = [self.coords.y]
        State.agent_colors= [self.color]
        box_colors = [None for _ in range(26)]
        goals = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        goals[goal_coords.x][goal_coords.y] = '0'
        State.walls = walls
        State.box_colors = box_colors
        State.goals = goals
        return State(agent_rows, agent_cols, boxes)

    def create_box_state(self,goal_coords,box_name,box_coords,walls,num_cols,num_rows):
        boxes = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        boxes[box_coords.x][box_coords.y] = box_name
        agent_rows = [self.coords.x]
        agent_cols = [self.coords.y]
        State.agent_colors= [self.color]
        box_colors = [None for _ in range(26)]
        box_colors[ord(box_name)-ord('A')] = self.color
        goals = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        goals[goal_coords.x][goal_coords.y] = box_name
        State.walls = walls
        State.box_colors = box_colors
        State.goals = goals
        return State(agent_rows, agent_cols, boxes)