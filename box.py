class Box:
    def __init__(self,name,color:'Color',coords:'Coords'):
        self.name = name
        self.coords = coords
        self.color = color
        self.on_goal = False
    
    def moved_to_goal(self):
        self.on_goal = True

    def __eq__(self,other):
        if isinstance(other,Box):
            return self.coords == other.coords and self.name == other.name
        else:
            return False
