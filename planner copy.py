from agent import TaskType
from coords import Coords
class Planner:
    def __init__(self,level):
        self.level = level
        self.pan = []
        self.plans=[]
        self.curr_plans=[]
        self.has_unfinished_goals = True
        self.assigned_agents = []
        self.assigned_boxes  = []
        self.temp_wall=[]
        self.removed_edges = []
        self.removed_nodes = []

    def check_unfinished_goals(self):
        for goal in self.level.box_goals:
            if not goal.is_done:
                return True
        for goal in self.level.agent_goals:
            if not goal.is_done:
                return True
        return False
        

    def get_plan(self):
        while self.check_unfinished_goals():
            agents ={}
            self.assigned_agents = []
            self.assigned_boxes = []
            self.assign_box_goals()
            self.assign_agent_goals()
            curr_goals = []
        #print('#Inside goals.'+str(len(self.level.agent_goals)), flush=True)
            for goal in self.level.box_goals:
                if goal.is_done:
                    continue
            #print('#adding move box '+str(goal.box.name)+' to agent :'+str(goal.agent.name), flush=True)
                if goal.has_agent:
                    curr_goals.append(goal)
                    box_path_g = self.level.get_shortest_path(goal.box.coords,goal.coords)
                    box_path_b = []
                    agent_path_b = self.level.get_shortest_path(goal.agent.coords,goal.box.coords)
                    agent_path_b = agent_path_b[:len(agent_path_b)-1]
                    agent_path_g = self.level.get_shortest_path(Coords(agent_path_b[-1][0],agent_path_b[-1][1]),goal.coords)
                    agent_path = agent_path_b + agent_path_g[1:len(agent_path_g)-1]
                    for count in agent_path_b:
                        box_path_b.append(box_path_g[0])
                    box_path  = box_path_b+box_path_g[1:]
                    #goal.agent.add_move_box(goal.coords,self.level.walls,self.level.num_cols,self.level.num_rows,goal.box)
                    
                    print('#inside box goal agent path is:'+str(agent_path), flush=True)
                    print('#inside box goal box path is:'+str(box_path), flush=True)
                    status = self.check_box_conflict(agent_path,goal.box)
                    print('#conflict status '+str(status), flush=True)
                    if status[0] == 'N':
                        goal.finish_box_goal(box_path,agent_path)
                        goal.box.moved_to_goal()
                        curr_goals.remove(goal)
                        goal.box.coords = Coords(box_path[-1][0],box_path[-1][1])
                        goal.agent.coords = Coords(agent_path[-1][0],agent_path[-1][1])
                        if len(self.removed_nodes)>0:
                            self.level.graph.add_nodes_from(self.removed_nodes)
                            self.removed_nodes=[]
                        if len(self.removed_edges)>0:
                            self.level.graph.add_nodes_from(self.removed_edges)
                            self.removed_eddes=[]
                        for box in self.level.boxes:
                            print('#inside assign new boxCoords:'+str((box.coords.x,box.coords.y)), flush=True)
                        for agent in self.level.agents:
                            print('#inside assign new agentCoords:'+str((agent.coords.x,agent.coords.y)), flush=True)
                        
                    #if status[0] == 'BG' or '':
                    else:
                        node = (status[1].coords.x,status[1].coords.y)
                        self.removed_edges = list(self.level.graph.edges(node))
                        self.removed_nodes = [node]
                        self.level.graph.remove_node(node)
                    #if status[0] == 'B':
                       # goal.finish()

            

            for goal in self.level.agent_goals:
            #print('#adding move goal  to agent :'+str(goal.agent.name), flush=True)
                if goal.has_agent:
                    curr_goals.append(goal)
                    #goal.agent.add_move(goal.coords,self.level.walls,self.level.num_cols,self.level.num_rows)
                    agent_path = self.level.get_shortest_path(goal.agent.coords,goal.coords)
                    goal.finish_agent_goal(agent_path)
            
            for agent.in 
            
            #for agent in self.level.agents:
            #print('#Start agent search for getting plans '+str(agent.name), flush=True)
                #self.level.graph()
                
            
            
            #for agent in self.level.agents:
            #    curr_plan = agent.get_current_plan()
            #    path = agent.pre_coords.get_path(curr_plan)
            #    box_path = agent.curr_task.box.coords.get_box_path(curr_plan)
                prev_box_coord= agent.curr_task.box.coords
                prev_agent_coord = agent.coords
            #    print('#length of path: '+str(len(path)),flush=True)
            #    print('#length of plan: '+str(len(curr_plan)),flush=True)
            #    
            #    if status[0]=='N':
            #        agent.curr_task.box.coords = box_path[-1]
            #        agent.curr_task.box.moved_to_goal()
            #        agent.coords = path[-1]
            #    if status[0]=='BG':
            #        for goals in curr_goals:
            #            if goals.agent == agent:
            #                curr_goals.remove(goals)
            #        self.level.walls[status[1].coords.x][status[1].coords.y]=True

            #    for step in path:
            #        print('#Agent Path '+str((step.x,step.y)), flush=True)
            #    for step in curr_plan:
            #        print('#Agent Path '+str(step), flush=True)
            #    for step in box_path:
            #        print('#Box Path '+str((step.x,step.y)), flush=True)
            #   # self.curr_plans.append(self.get_current_plan())

            #    self.plans.append(agent.get_current_plan())
            #    for goal in curr_goals:
            #        goal.finish()
                


        #return self.plan
        
    def check_box_conflict(self,path,goal_box):
        for box in self.level.boxes:
            if box==goal_box:
                continue
            print('#inside conflict boxCoords:'+str((box.coords.x,box.coords.y)), flush=True)
            if (box.coords.x,box.coords.y) in path:
                if box.on_goal:
                    return ('BG',box)
                else:
                    return ('B',box)
            else:
                return ('N',None)

    def assign_agent_goals(self):
        #print('#inside agent assign agentName:'+str(self.level.agent_goals[0].coords.get_coords()), flush=True)
        for goal in self.level.agent_goals:
            if goal.is_done:
                continue
            curr_dist = 10000
            #print('#inside agent assign agentName:'+str(agent.name), flush=True)
            for agent in self.level.agents:
                if agent not in self.assigned_agents:
                    if goal.agentName == agent.name:
                        print('#inside agent assign agentName:'+str(agent.name), flush=True)
                        dist = self.hueristic_assign(goal.coords,agent.coords)
                        if dist<curr_dist:
                            curr_dist = dist
                            goal.add_agent(agent)
                            self.assigned_agents.append(agent)

    def assign_box_goals(self):
        box_added = []
        for goal in self.level.box_goals:
            if goal.is_done:
                continue
            curr_dist=10000
            for box in self.level.boxes:
                if box not in self.assigned_boxes:
                    if box.on_goal:
                        continue
                    if goal.boxName == box.name:
                        print('#inside box assgin boxName:'+str(goal.boxName), flush=True)
                        print('#inside box assign goalName:'+str(box.name), flush=True)
                        print('#inside box assign boxCoords:'+str((box.coords.x,box.coords.y)), flush=True)
                        print('#inside box assign boxStatus:'+str(box.on_goal), flush=True)
                        dist = self.hueristic_assign(goal.coords,box.coords)
                        if dist<curr_dist:
                            curr_dist = dist
                            goal.add_box(box)
                            self.assigned_boxes.append(box)
        for goal in self.level.box_goals:
            if goal.is_done:
                continue
            curr_dist =10000
            
            for agent in self.level.agents:
                if agent not in self.assigned_agents:
                    if agent.color == goal.box.color:
                        print('#inside agent box assign agent:'+str(agent.name), flush=True)
                        print('#inside agent box assign box:'+str(goal.box.name), flush=True)
                        dist = self.hueristic_assign(agent.coords,box.coords)
                        if dist<curr_dist:
                            curr_dist = dist
                            goal.add_agent(agent)
                            self.assigned_agents.append(agent)

                        
    def hueristic_assign(self,coord1,coord2):
        xdiff = abs(coord1.x - coord2.x)
        ydiff = abs(coord1.y - coord2.y)
        return (xdiff+ydiff)
            
                    
                
