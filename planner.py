#wfrom agent import TaskType
from coords import Coords
from action import Action,ActionType
class Planner:
    def __init__(self,level):
        self.current_time = 0
        self.level = level
        # self.pan = []
        self.plans=[]
        self.curr_plans=[]
        self.unfinished_goals = level.goals
        self.assigned_agents = []
        self.assigned_boxes  = []
        self.temp_wall=[]
        self.curr_goals = []
        self.removed_edges = []
        self.removed_nodes = []
        self.plan_pool = {}
        self.approved_plans = {}
        self.non_conflicting_plans={}


    def create_inital_plans(self):
        # For all goals, create an inital plan to solve from closest box.
        for goal in self.level.box_goals:
            if goal.is_done:
                continue
            # Get closest box
            closest_box = (none, 9999)
            for box in self.level.boxes:
                if box.name != goal.name:
                    continue
                # TODO THIS SHOULD BE PATH ACTUALLY 
                dist = get_heuristic_dist(box.coords, goal.coords)
                if dist < closest_box[1]:
                    closest_box = (box, dist)
            p = plan(box=box, goal=goal, start_time = current_time)
            self.plan_pool.append(p)


    def plan(self):
        for agent in self.agents:
            # Plan, distance, prioirty, path
            assigned_plan = (None, 9999, 0, None)
            for plan in self.plan_pool:
                if (plan.box.color != agent.color):
                    continue
                # TODO Set this correctly so agent is not on top of box
                path = get_shortest_path(agent.coords, plan.box.coords)
                # Prioritise priority value first
                if plan.priority > assigned_plan[2]:
                    assigned_plan = (plan, len(path), plan.priority, path)
                elif plan.priority == assigned_plan[2]:
                    if len(path) < assigned_plan[1]:
                        assigned_plan = (plan, len(path), plan.priority, path)
                else:
                    # Plan is less important
                    continue
            # TODO Set this correctly so agent is not on top of box
            assigned_plan[0].start_coords = path[0]
            assigned_plan[0].end_coords = path[-1]
            agent.plans.append(assigned_plan[0])
                
    # First we are creating generic plans:
    # E.g. Box -> Goal, no time path is defined yet.
    # Then we find the shortest time path to that plan

    def generate_move_plans(self):
        for agent in self.agents:
            current_plan = agent.plans[0]
            if (agent.coords != curr_plan.start_coords):
                # create new plan to path
                tempPath = get_shortest_time_path(agent.coords, plan.box.coords, current_time)
                tempPlan = plan(agent=agent, box=current_plan.box, path=path)
                agent.plans.insert(tempPlan, 0)
                continue
            # check versus other agents plans and create conflict tuples
            otherAgents = self.agents[:]
            otherAgents.pop(agent)
            for otherAgent in otherAgents:
                for otherPlan in otherAgent.plans:
                    if plan.start_time == None:
                        continue
                    # This is a list of time coordinates that exists in both paths
                    conflict_set = find_conflicts(current_plan.path, otherPlan.path)
                    if (len(conflict_set) > 0):
                        # TODO Deal with conflict
                        # TODO alternative path
                        # TODO Waiting on path
                        


    def find_conflicts(self, timePath1, timePath2):
        return set(timePath1).intersection(timePath2)


    def assign_paths(self):
        for agent in self.agents:
            curr_plan = agent.plans[0]
            if (agent.coords != curr_plan.start_coords):
                path = get_shortest_time_path(agent.coords, curr_plan.start_coords)
                p = plan()



        # for plan in self.plan_pool:
        #     # Agent, distance value, path
        #     closest_agent = (none, 9999, none)
        #     for agent in self.level.agents:
        #         if agent.color != plan.box.color:
        #             continue
        #         path = get_shortest_path(agent.coords, box.coords)
        #         if len(dist) > closest_agent[1]:
        #             closest_agent = (agent, len(path), path)
        #     plan.agent, plan.length, plan.path = closest_agent




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

    def get_plan(self):
        while len(self.unfinished_goals)>0:
            self.do_assignment()
            self.search_paths()
            self.get_joint_action()
            for agent in self.assigned_agents:
                print('#Agent path for agent :.'+str(agent.name)+' is :'+str(agent.agent_path), flush=True)
                print('#Box path for agent :.'+str(agent.name)+' is :'+str(agent.box_path), flush=True)
                print('#Agent action for agent   :.'+str(agent.name)+' is :'+str(agent.plan), flush=True)
            self.reset_all()
            
            #self.get_joint_action()

    def get_joint_action(self):
        for agent in self.assigned_agents:
            box_path = agent.box_path
            agent_path = agent.agent_path
            actions = []
            for i in range(len(agent_path)-1):
                ard = agent_path[i][0]-agent_path[i+1][0]
                acd = agent_path[i][1]-agent_path[i+1][1]
                brd = box_path[i][0] - box_path[i+1][0]
                bcd = box_path[i][0] - box_path[i+1][0]
                if acd == 0 and ard == 0:
                    for action in Action:
                        if action.type == ActionType.NoOp:
                            actions.append(action)
                elif bcd == 0 and brd == 0:
                    for action in Action:
                        if action.type == ActionType.Move and action.agent_row_delta==ard and action.agent_col_delta==acd:
                            actions.append(action)
                else:
                    if agent_path[i+1] == box_path[i]:
                        for action in Action:
                            if action.type == ActionType.Push and action.agent_row_delta==ard and action.agent_col_delta==acd and action.box_row_delta==brd and action.box_col_delta == bcd:
                                actions.append(action)
                    else:
                        for action in Action:
                            if action.type == ActionType.Pull and action.agent_row_delta==ard and action.agent_col_delta==acd and action.box_row_delta==brd and action.box_col_delta == bcd:
                                actions.append(action)
            agent.plan = actions

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

    def get_closest_unassigned_agent(self,box):
        curr_dist=10000
        curr_agent = False
        for agent in self.level.agents:
            if agent not in self.assigned_agents:
                if box.color == agent.color:
                    dist = self.get_heuristic_dist(box.coords,agent.coords)
                    if dist<curr_dist:
                        curr_agent = agent
                        curr_dist = dist
        return curr_agent


    def get_heuristic_dist(self,coorda,coordb):
        xdist = abs(coorda[0]-coordb[0])
        ydist = abs(coorda[1]-coordb[1])
        return (xdist+ydist)

        
    def get_move_action(self,ard,acd):
        if ard == 1:
            return Action("Move(S)", ActionType.Move, ard, acd, 0, 0)
        elif ard == -1: 
            return Action("Move(N)", ActionType.Move, ard, acd, 0, 0)
        elif acd ==  1:
            return Action("Move(E)", ActionType.Move, ard, acd, 0, 0)
        elif acd == -1:
            return Action("Move(W)", ActionType.Move, ard, acd, 0,0)
        else:
            return Action("NoOp", ActionType.NoOp, 0, 0, 0, 0)



    def get_push_action(self,ard,acd,brd,bcd):
        if ard == -1 and brd==1:
            return Action("Push(N,N)", ActionType.Push, -1, 0, -1, 0)
        if ard == -1 and bcd == 1:
            return Action("Push(N,E)", ActionType.Push, -1, 0, 0, 1)
        if ard == -1 and bcd==-1:
            return Action("Push(N,W)", ActionType.Push, -1, 0, 0, -1)
        if ard == 1 and brd==1:
            return Action("Push(S,S)", ActionType.Push, 1, 0, 1, 0)
        if ard == 1 and bcd==1:
            return Action("Push(S,E)", ActionType.Push, 1, 0, 0, 1)
        if ard == 1 and bcd == -1:
            return Action("Push(S,W)", ActionType.Push, 1, 0, 0, -1)
        if acd == 1 and bcd==1:
            return Action("Push(E,E)", ActionType.Push, 0, 1, 0, 1)
        if acd == 1 and brd == -1:
            return Action("Push(E,N)", ActionType.Push, 0, 1, -1, 0)
        if acd == 1 and brd == 1:
            return Action("Push(E,S)", ActionType.Push, 0, 1, 1, 0)
        if acd == -1 and bcd == -1:
            return Action("Push(W,W)", ActionType.Push, 0, -1, 0, -1)
        if acd == -1 and brd == 1:
            return Action("Push(W,S)", ActionType.Push, 0, -1, 1, 0)
        if acd == -1 and brd == -1:
            return Action("Push(W,N)", ActionType.Push, 0, -1, -1, 0)
        

    def get_pull_action(self,ard,acd,brd,bcd):
        if ard == -1 and brd==-1:
            return Action("Pull(N,N)", ActionType.Pull, -1, 0, -1, 0)

        if ard == -1 and bcd==1:
            return Action("Pull(N,E)", ActionType.Pull, -1, 0, 0, 1)

        if ard == -1 and bcd==-1:
            return Action("Pull(N,W)", ActionType.Pull, -1, 0, 0, -1)

        if ard == 1 and brd==1:
            return Action("Pull(S,S)", ActionType.Pull, 1, 0, 1, 0)

        if ard == 1 and bcd==1:
            return Action("Pull(S,E)", ActionType.Pull, 1, 0, 0, 1)

        if ard == 1 and bcd==-1:
            return Action("Pull(S,W)", ActionType.Pull, 1, 0, 0, -1)

        if acd == 1 and brd==1:
            return Action("Pull(E,E)", ActionType.Pull, 0, 1, 0, 1)

        if acd == 1 and brd==-1:
            return Action("Pull(E,N)", ActionType.Pull, 0, 1, -1, 0)

        if acd == 1 and brd==1:
            return Action("Pull(E,S)", ActionType.Pull, 0, 1, 1, 0)


        if acd == -1 and bcd==1:
            return Action("Pull(W,W)", ActionType.Pull, 0, -1, 0, -1)

        if acd == -1 and brd==-1:
            return Action("Pull(W,N)", ActionType.Pull, 0, -1, -1, 0)

        if ard == -1 and brd==1:
            return Action("Pull(W,S)", ActionType.Pull, 0, -1, 1, 0)