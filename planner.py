#wfrom agent import TaskType
from coords import Coords
from action import Action,ActionType
from plan import Plan
# from itertools import combinations
import itertools
from itertools import combinations, zip_longest

from conflictenum import ConflictEnum


def isNextTo(x, y, otherX, otherY):
    xdiff = abs(x - otherX)
    ydiff = abs(y - otherY)
    totaldiff = xdiff + ydiff
    if totaldiff == 1 :
        return True
    else:
        return False                 

class Planner:
    def __init__(self,level):
        self.current_time = 0
        self.level = level
        # self.pan = []
        self.plans=[]
        self.curr_plans=[]
        self.unfinished_goals = level.goals
        self.assigned_agents = set()
        self.assigned_boxes  = []
        self.temp_wall=[]
        self.curr_goals = []
        self.removed_edges = []
        self.removed_nodes = []
        self.plan_pool = set()
        self.approved_plans = set()
        self.non_conflicting_plans = set()

    def check_finished_goals(self):
        print('#checking finished goals',flush=True)
        for goal in self.level.goals:
            if goal.box_name == None:
                for agent in self.level.agents:
                    if agent.coords == goal.coords and agent.name == goal.agent_name:
                        goal.finish()
            else:
                for box in self.level.boxes:
                    if box.coords == goal.coords and box.name == goal.box_name:
                        goal.finish()


    def create_inital_plans(self):
        # For all goals, create an inital plan to solve from closest box.
        for goal in self.level.goals:
            if goal.box_name== None:
                tempPlan = Plan()
                tempPlan.setGoal(goal)
                tempPlan.priority = -1
                self.plan_pool.add(tempPlan)
                continue
            if goal.is_done:
                continue
            # Get closest box
            closest_box = (None, 9999, None)
            for box in self.level.boxes:
                if box.name != goal.box_name:
                    continue
                path = self.get_heuristic(box.coords, goal.coords)
                if path == None:
                    continue
                if len(path) < closest_box[1]:
                    closest_box = (box, len(path), path)
            tempPlan = Plan()
            tempPlan.setBox(closest_box[0])
            tempPlan.setGoal(goal)
            tempPlan.setStartTime(self.current_time)
            tempPlan.setBoxPath(closest_box[2])
            self.plan_pool.add(tempPlan)


    def determine_plan_priorities(self):
        # conflicts = {}
        for plan in self.plan_pool:
            if (plan.box == None):
                continue
            for coord in plan.box_path:
                if coord== plan.box_path[-1]:
                    break
                # TODO
                # for box in self.level.boxes:
                #     if (coord == box.coord):
                #         # Keep track of what boxes are on paths
                #         # so later we can up their prioirty plans
                #         if (box not in conflicts.keys()):
                #             conflicts[box] = 1
                #         else:
                #             conflicts[box] += 1
                if coord in self.level.goal_coords:
                    plan.priority += 1

    def get_plan_priority(self,path):
        priority = 1
        for coord in path:
            if coord== path[-1]:
                break
            if coord in self.level.goal_coords:
                priority += 1
        return priority



    def assign_initial_plans(self):
        self.temp_plan_pool = self.plan_pool.copy()
        while self.can_assign_plans():
            for plan in self.plan_pool:
                if plan.box == None:
                    continue
                if plan not in self.temp_plan_pool:
                    continue
                else:
                    agent = self.find_closest_agent(plan.box)
                    if not agent:
                        continue
                    if agent.plan==None :
                        plan.setAgent(agent)
                        agent.plan = plan
                        self.temp_plan_pool.remove(plan)
                        self.assigned_agents.add(agent)
                        continue
                    if (agent.plan.priority < plan.priority):
                        agent.plan.setAgent(None)
                        self.temp_plan_pool.add(agent.plan)
                        plan.setAgent(agent)
                        agent.plan = plan
                        self.temp_plan_pool.remove(plan)
                        continue
  #convvert plan to smaller plans 
    def create_initial_agent_plans(self):
        for agent in self.level.agents:
            if agent.plan != None:
                if agent.plan.box !=None:
                    if self.can_agent_do_plan(agent):
                        ## create agent path ()
                        # agent.plan.agent_path = self.get_shortest_path(agent.coords,agent.plan.goal.coords)[:-1]
                        paths = self.create_agent_path_off_box(agent.coords,agent.plan.box_path)
                        
                        agent.actions = paths[1]
                        agent.plan.agent_path = paths[0]
                        print(f'#list of actions: {paths[1]}')
                    path_to_box = self.get_shortest_path(agent.coords,agent.plan.box.coords)
                    path_to_box = path_to_box[:-1]
                    tempPlan = Plan()

                    #tempPlan.setGoal(agent.plan.goal)
                    tempPlan.setStartTime(self.current_time)
                    tempPlan.setAgentPath(path_to_box)
                    tempPlan.setAgent(agent)
                    #tempPlan.setGoal()
                    agent.next_plan = agent.plan
                    
                    agent.plan = tempPlan
                else:
                    print("Help Im stuck line in create_inital_agent_plans")

    def create_agent_path_off_box(self, agent_coord, box_path):
        temp_agent_coord = list(agent_coord)
        print(f"temp: {temp_agent_coord}")
        action_list = []
        agent_path = []
        agent_path.append(agent_coord)
        # N 0
        # S 1
        # E 2
        # W 3
        for i in range(len(box_path)-1):
            print(f'#Inputitng agruments {temp_agent_coord},{box_path[i]},{box_path[i+1]}')
            if i== len(box_path)-2:
                directions, tempAction = self.determine_action(tuple(temp_agent_coord), box_path[i], box_path[i+1],box_path[i+1])
            else:
                directions, tempAction = self.determine_action(tuple(temp_agent_coord), box_path[i], box_path[i+1],box_path[i+2])
           
            action_list.append(tempAction)
            #print(f'# action is {action_list}',flush = True)
            # temp_agent_coord[0] = 
            if (directions[0] == "0"):
                temp_agent_coord[0] -= 1
            elif (directions[0] == "1"):
                temp_agent_coord[0] += 1
            elif (directions[0] == "2"):
                temp_agent_coord[1] += 1
            elif (directions[0] == "3"):
                temp_agent_coord[1] -= 1
            else:
                pass
            agent_path.append(tuple(temp_agent_coord))


        return (agent_path, action_list)

    def assign_agent_goals(self):
        for goal in self.level.goals:
            # print(f"Goal.name :  goal.agentName : {goal.agentName}")
            if goal.box_name == None:
                #print("Inside agent goals")
                closest_agent = (None, 9999, None)
                for agent in self.level.agents:
                    #print(f"agent.name = {agent.name}")

                    if (agent.name != goal.agentName):
                        continue
                    if agent.plan != None:
                        continue
                    #print("assinging plans to aget")
                    path_to_goal = self.get_shortest_path(agent.coords, goal.coords)
                    len_path_to_goal = len(path_to_goal)
                    if (len_path_to_goal < closest_agent[1] ):
                        closest_agent = (agent, len_path_to_goal, path_to_goal)
                if (closest_agent[0] != None):
                    tempPlan = Plan()
                    tempPlan.setAgent(closest_agent[0])
                    tempPlan.setGoal(goal)
                    tempPlan.setAgentPath(closest_agent[2])
                    priority = self.get_plan_priority(closest_agent[2])
                    tempPlan.priority = priority

                    closest_agent[0].plan = tempPlan

                    self.plan_pool.add(tempPlan)
                    # Add to plan list now?

    def find_closest_agent(self,box):
        curr_dist=10000
        curr_agent = None
        for agent in self.level.agents:
            if agent not in self.assigned_agents:
                if box.color == agent.color:
                    dist = len(self.get_heuristic(box.coords,agent.coords))
                    if dist<curr_dist:
                        curr_agent = agent
                        curr_dist = dist
        return curr_agent

    def can_assign_plans(self):
        for agent in self.level.agents:
            if agent not in self.assigned_agents:
                for plan in self.plan_pool:
                    if plan.box != None:
                        if plan.box.color == agent.color:
                            return True
                    elif plan.goal.agentName == agent.name:
                        return True
                    else:
                        pass
        return False

    def move_boxes(self):
        for agent in self.level.agents:
            if agent.plan !=None:
                if agent.plan.box != None:
                    if agent.plan.agent_path == None:
                        agent.plan.agent_path  = self.move_box(agent.plan)
                        pass
                        


    def move_box(self, plan):
        # Assumption, we are always trying to push the box
        agent_path = self.get_shortest_path(plan.agent.coords, plan.goal.coords)[:-1]
        box_path = plan.box_path
        # if agent_path == box_path Only push
        # if box_path - agent_path = 2
        if (len(agent_path) == len(box_path)):
            return agent_path
        elif (len(box_path) - len(box_path) == 2):
            return False
        else:
            return False
        # for agent_coord, box_path in zip(agent_path, box_path):
        #     action_type = self.get_action_type(agent_coord,box_path)


                    
    
    
                    
                        
    def find_same_cell_conflicts(self, timePath1, timePath2):
        return list(set(timePath1).intersection(timePath2))

    def find_swapping_cell_conflicts(self, timePath1, timePath2):
        for timeCoord in timePath1:
            tempConflicts = []
            for otherTimeCoord in timePath2:
                if (abs(timeCoord[1] - otherTimeCoord[1]) == 1):
                    if (timeCoord[0] == otherTimeCoord[0]):
                        tempConflicts.append([timeCoord, otherTimeCoord])
        return tempConflicts

    def find_swapping(self, plan_list):
        plan_combinations = itertools.combinations(plan_list, 2)
        all_conflicts = []
        for plan1, plan2 in plan_combinations:
            conflicts = self.find_swapping_cell_conflicts(plan1.path, plan2.path)
            minSwappingConflicts = min(conflicts, key=lambda x: (x[0][1], x[1][1]))
            all_conflicts.append((ConflictEnum.SwappingCells, (plan1, plan2), [minSwappingConflicts]))

        return all_conflicts

    def find_conflicts_from_plans(self, plan_list):
        normal_conflicts = []
        swapping_conflicts = []
        plan_combinations = itertools.combinations(plan_list, 2)
        for plan1, plan2 in plan_combinations:
            conflicts = self.find_same_cell_conflicts(plan1.path, plan2.path)
            if (len(conflicts) > 0):
                minConflict = min(conflicts, key=lambda x: x[1])
                normal_conflicts.append((ConflictEnum.SameCell,(plan1,plan2),[minConflict]))

            swappingConflicts = self.find_swapping_cell_conflicts(plan1.path, plan2.path)
            if (len(swappingConflicts) > 0):
                minSwappingConflicts = min(swappingConflicts, key=lambda x: (x[0][1], x[1][1]))
                swapping_conflicts.append((ConflictEnum.SwappingCells, (plan1, plan2), [minSwappingConflicts]))

        ln = len(normal_conflicts)
        ls = len(swapping_conflicts)
        if (ln > 0 and ls == 0):
            return normal_conflicts
        elif (ls > 0 and ls == 0):
            return swapping_conflicts
        elif (ln == 0 and ls == 0):
            return []
        else:
            if (normal_conflicts[0][2][2] <= swapping_conflicts[0][2][0][1] + swapping_conflicts[0][2][1][1]):
                return normal_conflicts
            else:
                return swapping_conflicts
        return []

    def assign_paths(self):
        for agent in self.agents:
            curr_plan = agent.plans[0]
            if (agent.coords != curr_plan.start_coords):
                path = self.get_shortest_time_path(agent.coords, curr_plan.start_coords)
                p = plan()
                # TODO????????????????????????????????????????????????????????????????


    def get_on_time_path_objects(self, path):
        tempDict = {}
        for coords, time in path:
            for box in self.level.boxes:
                if coords == box.coords:
                    tempDict[box] = coords
            for boxGoal in self.level.goals:
                if coords == boxGoal.coords:
                    tempDict[goal] = coords
        return tempDict


    def check_unfinished_goals(self):
        for goal in self.level.box_goals:
            if not goal.is_done:
                return True
        for goal in self.level.agent_goals:
            if not goal.is_done:
                return True
        return False


    def reset_all(self):
        for goal in  self.curr_goals:
                goal.agent.reset_agent()
        self.curr_goals = []
        self.assigned_agents=[]
#main planner method
    def get_plan(self):
        #while len(self.unfinished_goals)>0:
        # Marks the already done goals as done
        self.check_finished_goals()

        # Makes initial plans with goals assigned  
        self.create_inital_plans()
        # Assings priorities to all inital plans
        self.determine_plan_priorities()

        # for plan in self.plan_pool:
            # print('#Plan for box: '+str(plan.box.name)+' at :'+str(plan.box.coords)+ 'for goal at : '+str(plan.goal.coords)+'path is: '+str(plan.box_path), flush=True)
        self.assign_initial_plans() # assigns the plans to agents
        
        # CHECK AGENT IS ON PLAN START
        #  if not -> split plan Agent -> start, box -> goal

        
        
        self.create_initial_agent_plans() #splits box plans of agents into two plans and converts assingn priority to new plan next_plan and plan is way to creatting local partial order for agents
        self.assign_agent_goals()
        #self.get_joint_actions()
        #self.plan()
        for agent in self.level.agents:
            if (agent.plan != None):
                if agent.plan.box==None:
                    print('#Plan for agent: '+str(agent.name)+' at :'+str(agent.coords)+ 'for goal at : ', flush=True)
                else:
                    print('#Plan for agent: '+str(agent.name)+' at :'+str(agent.coords)+'for box:'+str(plan.box.name) +'at : '+str(plan.box.coords)+'for goal at :', flush=True)   
        while len(self.unfinished_goals)>0:
            self.move_boxes()
            for agent in self.level.agents:
                if agent.plan!=None:
                    agent.create_timed_plan()

            for agent in self.level.agents:
                if agent.plan!=None:
                    print(f'#############UNFINISHED GOALS LEFT {len(self.unfinished_goals)}')
                    print('#Plan for agent: '+str(agent.name)+' at :'+str(agent.coords)+ 'for goal at : '+str(agent.plan.agent_path), flush=True)
                    self.finalize_plan(agent)
                    self.get_agent_new_plan(agent)
                    print("I am out of there!")

        self.get_joint_actions()
        



        
        #checking_interval =get_shortest_plan()
        #find conflicts in checking_interval
        

        #for agent in self.level.agents:
            #print(f'Agent: {agent}, Plan: {str()}')
            #self.search_paths()
            #self.get_joint_action()
            #for agent in self.assigned_agents:
            #    print('#Agent path for agent :.'+str(agent.name)+' is :'+str(agent.agent_path), flush=True)
            #    print('#Box path for agent :.'+str(agent.name)+' is :'+str(agent.box_path), flush=True)
            #    print('#Agent action for agent   :.'+str(agent.name)+' is :'+str(agent.plan), flush=True)
            #self.reset_all()
            
            #self.get_joint_action()

    def get_agent_new_plan(self, agent):
        priority_list = []
        priority_plan = -9999
        for plan in self.plan_pool:
            if plan.agent != None:
                continue
            try:
                if plan.box.color == agent.color:
                    if (plan.priority > priority_plan):
                        priority_list = []
                        priority_plan = plan.priority
                        priority_list.append(plan)
                    elif (plan.priority == priority_plan):
                        priority_list.append(plan)
                    else:
                        continue
            except AttributeError:
                if plan.goal.agentName == agent.name:
                    if (plan.priority > priority_plan):
                        priority_list = []
                        priority_plan = plan.priority
                        priority_list.append(plan)
                    elif (plan.priority == priority_plan):
                        priority_list.append(plan)
                    else:
                        continue
            except:
                continue


        closest_plan = (plan, 9999)
        for plan in priority_list:
# self.get_shortest_path(agent.coords,agent.plan.goal.coords)[:-1]
            path = self.get_shortest_path(agent.coords, plan.goal.coords)
            lPath = len(path)
            if (lPath < closest_plan[1]):
                closest_plan = (plan, lPath)
        
        closest_plan[0].agent = agent
        agent.plan = closest_plan[0]
        
            


    def can_agent_do_plan(self, agent):
        for agent in self.level.agents:
            if (agent.plan == None):
                return False
            if (agent.plan.box != None):
                if (len(agent.coords) == 2 and len(agent.plan.box.coords) == 2):
                    return isNextTo(*agent.coords, *agent.plan.box.coords)
            return False

    def finalize_plan(self,agent):
        #print('#agent name for goal is :'+str(agent.plan.goal.coords),flush=True)
        if agent.plan.goal!=None:
            print(f'#agent {agent.name} for goal is :'+str(agent.plan.goal),flush=True)
            print(f'#agent {agent.name} for goal is :'+str(self.unfinished_goals),flush=True)
            agent.plan.goal.is_done = True
            self.unfinished_goals.remove(agent.plan.goal)
            self.plan_pool.remove(agent.plan)
            self.assigned_agents.remove(agent)
        print('#finalising current_plan',flush=True)
        agent.finalize_curr_plan()
        print(f'agentPlan: {agent.plan}')
    
    def get_next_plan(self,agent):
        highest_priority_plan = (None, -9999)
        for plan in self.plan_pool:
            if (plan.prioirty > highest_priority_plan[1]):
                highest_priority_plan = (plan, plan.priority)
        
        # for agent in self.level.agents:
        #     if (agent.)
            



    def get_joint_actions(self):
        for agent in self.level.agents:
            
            agent_path = agent.final_path
            for i in range(len(agent_path)-1):
                if agent.actions :
                    continue
                # agent_coor = agent_path[1][0]
                # box_coord = agent_path[i][1]
                # box_next_coord = agent_path[i+1][1]

                ard = agent_path[i+1][0][0]-agent_path[i][0][0]
                acd = agent_path[i+1][0][1]-agent_path[i][0][1]
                # print("#agent_row_delta : "+str(ard),flush = True)
                # print("#agent_col _delta : "+str(acd),flush = True)
                if agent_path[i][1][0] == None:
                    brd=0
                    bcd=0
                else:
                    brd = agent_path[i+1][1][0] - agent_path[i][1][0]
                    bcd = agent_path[i+1][1][1]- agent_path[i][1][1]
                if acd == 0 and ard == 0:
                    for action in Action:
                        if action.type == ActionType.NoOp:
                            agent.actions.append(action)
                elif bcd == 0 and brd == 0:
                    for action in Action:
                        if action.type == ActionType.Move and action.agent_row_delta==ard and action.agent_col_delta==acd:
                            agent.actions.append(action)
                else:
                    # action = self.determine_action(agent_path[i][0], agent_path[i][1], agent_path[i+1][1])
                    # agent.actions.append(action)
                    if agent_path[i+1][1] == agent_path[i][0]:
                        for action in Action:
                            if action.type == ActionType.Push and action.agent_row_delta==ard and action.agent_col_delta==acd and action.box_row_delta==brd and action.box_col_delta == bcd:
                                agent.actions.append(action)
                    else:
                        for action in Action:
                            if action.type == ActionType.Pull and action.agent_row_delta==ard and action.agent_col_delta==acd and action.box_row_delta==brd and action.box_col_delta == bcd:
                                agent.actions.append(action)
            
            
            agent_ordering = [None for x in self.level.agents]
            for agent in self.level.agents:
                agent_ordering[ord(agent.name)-ord('0')] = agent
        
            # itertools.zip_longest(*list_of_actions, fillvalue="")

            #print()

            list_of_actions = []
            print(f'#lenght :::{len(agent_ordering)}',flush=True)
            
            for agent in agent_ordering:
                list_of_actions.append(agent.actions)
                print('######ACTIONS FOR AGENT######## '+str(agent.name)+'are: '+str(agent.actions),flush =True)
            if len(agent_ordering)>1:
                self.joint_action = list(itertools.zip_longest(*list_of_actions, fillvalue=Action.NoOp))
            else:
                self.joint_action = agent_ordering[0].actions
                for i in range(len(self.joint_action)):
                    self.joint_action[i] = [self.joint_action[i]]
            # """ self.joint_action = []
            # agents_left = len(agent_ordering)
            # while agents_left>0:
            #     joint_step=[]
            #     for agent in agent_ordering:
            #         if agent.has_next_action():
            #             action = agent.actions.popleft()
            #             print(action)
            #         else:
            #             action = Action.NoOp
            #             agents_left-=1
            #         joint_step.append(action)
            #     self.joint_action.append(joint_step) """
        print('#'+str(self.joint_action),flush =True)
 
        
    def determine_action(self, agent_coord, box_coord, box_next_coord,box_next_next_coord):
        # WARNING, COORDINATES ARE FLIPPED HERE (COL, ROW) (X, Y)
        actions = (ActionType.Push, ActionType.Pull)
        pull = False
        # directions = {"North", "South", "East", "West"}
                            # 0       1       2       3
        # Determine direction

        pullActionList = { "22" : Action.PullEE,
                       "20": Action.PullEN,
                       "21": Action.PullES,
                       "11" : Action.PullSS,
                       "12": Action.PullSE,
                       "13": Action.PullSW,
                       "00" : Action.PullNN,
                       "03": Action.PullNW,
                       "02": Action.PullNE,
                       "33" : Action.PullWW,
                       "30": Action.PullWN,
                       "31":Action.PullWS }

        pushActionList = { "22" : Action.PushEE,
                       "20": Action.PushEN,
                       "21": Action.PushES,
                       "11" : Action.PushSS,
                       "12": Action.PushSE,
                       "13": Action.PushSW,
                       "00" : Action.PushNN,
                       "03": Action.PushNW,
                       "02": Action.PushNE,
                       "33" : Action.PushWW,
                       "30": Action.PushWN,
                       "31":Action.PushWS }
        
        dBoxRow = box_next_coord[0] - box_coord[0]
        dBoxCol = box_next_coord[1] - box_coord[1]



        if (dBoxCol == 1):
            # East
            direction = 2
        elif (dBoxRow == 1):
            # South
            direction = 1
        elif (dBoxRow == -1):
            # North
            direction = 0
        else:
            # West
            direction = 3
        if (agent_coord == box_next_coord):
            pull = True
            changed = False
            row= agent_coord[0]
            col = agent_coord[1]
            coords_list = [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
            dAgentRow = box_next_next_coord[0] - agent_coord[0]
            dAgentCol = box_next_next_coord[1] - agent_coord[1]
            for coord in coords_list:
                if not (coord == box_next_next_coord or self.checkIfWall(coord) or coord == box_coord or coord == box_next_coord) and changed == False:
                    print(f'#{coord}', flush=True)
                    dAgentRow = coord[0] - agent_coord[0]
                    dAgentCol = coord[1] - agent_coord[1]
                    print(f'#{dAgentRow},{dAgentCol}', flush=True)
                    changed = True
                    # agent_coord = coord

        else:
            dAgentRow = box_coord[0] - agent_coord[0]
            dAgentCol = box_coord[1] - agent_coord[1]



        # (y, x)
    
        if (dAgentCol == 1):
            # East
            if (pull):
                if not (self.checkIfWall((box_coord[0]-1, box_coord[1]))):
                    # PULL NE
                    aDirection=0
                elif not(self.checkIfWall((box_coord[0]+1, box_coord[1]))):
                    # PULL SE
                    aDirection=1
                else:
                    # PULL EE
                    aDirection=2
            aDirection = 2
        elif (dAgentRow == 1):
            # South
            if (pull):
                if not (self.checkIfWall((box_coord[0], box_coord[1]+1))):
                    # PULL ES
                    aDirection=2
                elif not(self.checkIfWall((box_coord[0], box_coord[1]-1))):
                    # PULL WS
                    aDirection=3
                else:
                    # PULL SS
                    aDirection=1
            aDirection = 1
        elif (dAgentRow == -1):
            # North
            if (pull):
                if not(self.checkIfWall((box_coord[0], box_coord[1]+1))):
                    # PULL EN
                    aDirection=2
                elif not(self.checkIfWall((box_coord[0], box_coord[1]-1))):
                    # PULL WN
                    aDrection=3
                else:
                    # PULL NN
                    aDirection=0
            aDirection = 0
        else:
            # West
            if (pull):
                if not(self.checkIfWall((box_coord[0]-1,box_coord[1]))):
                    # PULL NW
                    aDirection=0
                elif not(self.checkIfWall((box_coord[0]+1,box_coord[1]))):
                    # PULL SW
                    aDirection=1
                else:
                    # PULL WW
                    aDirection=3
            aDirection = 3
        if (pull):
            return f"{aDirection}{direction}",pullActionList[f"{aDirection}{direction}"]
        return f"{aDirection}{direction}",pushActionList[f"{aDirection}{direction}"]

    def checkIfWall(self, coord):
        if coord[0] > self.level.num_rows or coord[0] < 0:
            return True
        elif coord[1] > self.level.num_cols or coord[1] < 0:
            return True
        else:
            return self.level.walls[coord[0]][coord[1]]
        


        # if (dAgentCol == 1):
        #     # East
        #     if (direction == 2):
        #         # PULL
        #         return Action.PullEE
        #     else:
        #         if (dAgentRow == 1):
        #             actionList(str(12))
        #         else:

        #         # Push
        # elif (dAgentRow == 1):
        #     # South
        #     if (direction == 1):
        #         # PULL
        #         return Action.PullSS
        #     else:
        #         # PUSH
        # elif (dAgentRow == -1):
        #     # North
        #     if (direction == 0):
        #         return Action.PullNN
        #     else:
        #         # PUSH
        # else:
        #     # West
        #     if (directon == 3):
        #         return Action.PullWW
        #     else:
        #         # PUSH
            
        

    def get_agent_box_actions(agent_path, box_path):
        action_list = []



        for i in range(len(agent_path)-1):
            ard = agent_path[i+1][0][0]-agent_path[i][0][0]
            acd = agent_path[i+1][0][1]-agent_path[i][0][1]
            print("#agent_row_delta : "+str(ard),flush = True)
            print("#agent_col _delta : "+str(acd),flush = True)
            if agent_path[i][1][0] == None:
                brd=0
                bcd=0
            else:
                brd = agent_path[i+1][1][0] - agent_path[i][1][0]
                bcd = agent_path[i+1][1][1]- agent_path[i][1][1]
            if acd == 0 and ard == 0:
                for action in Action:
                    if action.type == ActionType.NoOp:
                        agent.actions.append(action)
            elif bcd == 0 and brd == 0:
                for action in Action:
                    if action.type == ActionType.Move and action.agent_row_delta==ard and action.agent_col_delta==acd:
                        agent.actions.append(action)
            else:
                if agent_path[i+1] == agent.plan.box_path[i]:
                    for action in Action:
                        if action.type == ActionType.Push and action.agent_row_delta==ard and action.agent_col_delta==acd and action.box_row_delta==brd and action.box_col_delta == bcd:
                            agent.actions.append(action)
                else:
                    for action in Action:
                        if action.type == ActionType.Pull and action.agent_row_delta==ard and action.agent_col_delta==acd and action.box_row_delta==brd and action.box_col_delta == bcd:
                            agent.actions.append(action)


                



            #agent.plan_actions = actions

    def do_assignment(self):
        #self.curr_goals = []
        for goal in self.unfinished_goals:
            #print('#goal :.'+str(goal), flush=True)
            if not(goal.box_name == None):
                box = self.get_closest_unassigned_box(goal)
                agent = self.get_closest_unassigned_agent(box)
                if box and agent:
                    goal.add_box(box)
                    print('#Assigned Box :.'+str(box.name)+' at :'+str(box.coords)+'to Goal at:'+str(goal.coords), flush=True)
                    agent = self.get_closest_unassigned_agent(box)
                    self.assigned_boxes.append(box)
                    self.assigned_agents.append(agent)
                    goal.add_agent(agent)
                    print('#Assigned Box :.'+str(box.name)+'at :'+str(box.coords)+'to agent at:'+str(agent.coords), flush=True)
                    #self.unfinished_goals.remove(goal)
                    print('#Unfinished Goals not found :.'+str(len(self.unfinished_goals)),flush=True)
                    self.curr_goals.append(goal)

    def search_paths(self):
        for goal in self.curr_goals:
            if not(goal.box_name == None):
                path = self.get_agent_box_path(goal.agent.coords,goal.box.coords,goal.coords)
            else:
                path = self.get_agent_path(goal.agent.coords,goal.coords)
            self.unfinished_goals.remove(goal)
            #print('#Unfinished Goals not found :.'+str(goal.box_name), flush=True)
            goal.agent.add_paths(path) 
    

    def get_shortest_path(self, coord1, coord2):
        path = self.level.get_shortest_path(coord1, coord2)
        return path

    def get_shortest_time_path(self, coord1, coord2, start_time):
        path = self.level.get_shortest_path(coord1, coord2, start_time)
        return path

    def get_agent_box_path(self,agent_coords,box_coords,goal_coords):
        box_path_g = self.level.get_shortest_path(box_coords,goal_coords)
        box_path_b = []
        agent_path_b = self.level.get_shortest_path(agent_coords,box_coords)
        agent_path_b = agent_path_b[:len(agent_path_b)-1]
        agent_path_g = self.level.get_shortest_path((agent_path_b[-1][0],agent_path_b[-1][1]),goal_coords)
        agent_path = agent_path_b + agent_path_g[1:len(agent_path_g)-1]
        for count in agent_path_b:
            box_path_b.append(box_path_g[0])
            box_path  = box_path_b+box_path_g[1:]
        return [agent_path,box_path]

    def get_agent_path(self,agent_coords,goal_coords):
        agent_path = self.level.get_shortest_path(agent_coords,goal_coords)
        return [agent_path,None]




    def get_closest_unassigned_box(self,goal):
        curr_dist=10000
        curr_box = False
        for box in self.level.boxes:
            if box not in self.assigned_boxes:
                if box.name == goal.box_name:
                    dist = self.get_heuristic_dist(goal.coords,box.coords)
                    if dist<curr_dist:
                        cnurr_box = box
                        curr_dist = dist
        return curr_box



    def get_heuristic(self,coorda,coordb):
        try:
            return(self.level.get_shortest_path(coorda,coordb))
        except:
            return(None)