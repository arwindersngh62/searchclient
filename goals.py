class Goal:
    def __init__(self,coords:'Coords'):
        self.coords = coords
        self.agentName = None
        self.is_done = False
        self.has_agent = False
        self.box_name = None
        self.has_box = False
        
    def add_agent(self,agent:'Agent'):
        self.agent = agent
        self.has_agent = True
    
    def add_box(self,box:'Box'):
        self.box = box
        self.has_box = True

    def finish_agent_goal(self,agent_path):
        self.is_done=True
        self.agent.add_agent_path(agent_path) 

    def add_box_name(self,name):    
        self.box_name = name
    
    def add_agent_name(self,name):
        self.agent_name = name

    def reset_goal(self):
        self.has_agent = False
        self.box = None

    def __eq__(self,other):
        if isinstance(other,Goal):
            return (self.coords == other.coords and self.box_name == other.box_name)
