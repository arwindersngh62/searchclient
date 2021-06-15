import networkx as nx
from coords import Coords
class Level:
    def __init__(self,agents,boxes,goals,walls,num_cols,num_rows):
        self.agents = agents
        self.boxes = boxes
        self.goals = goals
        self.walls = walls
        self.num_cols = num_cols
        self.num_rows = num_rows
        #self.goal_coords=[]
        self.get_goal_coords()

    def get_boxes():
        return self.boxes

    def get_box_goals():
        return self.box_goals

    def get_agents():
        return self.agents

    def get_agent_goals():
        return self.agent_goals

    def get_walls():
        return self.walls


    def get_goal_coords(self):
        self.goal_coords=[]
        for goal in self.goals:
            self.goal_coords.append(goal.coords)

    def get_next_nodes(self,node):
        return [(node[0],node[1]+1),(node[0]+1,node[1]),(node[0]-1,node[1]),(node[0],node[1]-1)]

    def generate_graph(self):
        self.graph = nx.Graph()
        self.corridor_nodes=[]
        self.corridor_starts=[]
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if not(self.walls[row][col]):
                    self.graph.add_node((row,col),node_type='room')
        for node in self.graph.nodes:
            next = self.get_next_nodes(node)
            for i in next:
                #print('#edge: '+str(i in self.graph.nodes),flush=True)
                if i in self.graph.nodes:
                    self.graph.add_edge(node,i)
        for node in self.graph.nodes:
            if node not in self.corridor_nodes:
                self.corridor_nodes.append(node)
            if self.graph.degree[node] == 2:    
                next = self.graph.adj[node]
                for ne_next in next:
                    #print('#edge: '+str(ne_next),flush=True)
                    if self.graph.degree[ne_next] == 2:
                        if ne_next not in self.corridor_nodes:
                            self.corridor_nodes.append(ne_next)
                    elif self.graph.degree[ne_next] > 2:
                        if ne_next not in self.corridor_starts:
                            self.corridor_starts.append(ne_next)
        print('#corridor nodes: '+str(self.corridor_nodes),flush=True)
        print('#corridor starts: '+str(self.corridor_starts),flush=True)

    def get_shortest_path(self,node1,node2):
        s_path = nx.dijkstra_path(self.graph,node1,node2)
        return (s_path)

    def get_shortest_time_path(self, coord1, coord2, start_time):
        s_path = nx.dijkstra_path(self.graph,node1,node2)
        time = range(start_time, start_time+len(s_path))
        return list(zip(s_path, time))



   