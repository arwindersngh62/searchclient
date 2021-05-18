class Coords:
    def __init__(self,x:'int',y:'int'):
        self.x = x
        self.y = y

    def apply_action(self, action:'Action'):
        newx = self.x + action.agent_row_delta
        newy = self.y + action.agent_col_delta
        return (Coords(newx,newy))

    def apply_box_action(self, action:'Action'):
        newx = self.x + action.box_row_delta
        newy = self.y + action.box_col_delta
        return (Coords(newx,newy))

    def is_next_to(self, coord : 'Coords'):
        xdiff = abs(self.x - coord.x)
        ydiff = abs(self.y - coord.y)
        totaldiff = xdiff + ydiff
        if totaldiff == 1 :
            return True
        else:
            return False

    def get_coords(self):
        return((self.x,self.y))

    def get_path(self,action_list):
        path = [self]
        curr_coord=self
        for action in action_list:
            #print('#Start agent search for getting plans '+str(action[0].type), flush=True)
            curr_coord = curr_coord.apply_action(action[0])
            path.append(curr_coord)
        return(path)

    def get_box_path(self,action_list):
        path = [self]
        curr_coord=self
        for action in action_list:
            #print('#Start agent search for getting plans '+str(action[0].type), flush=True)
            curr_coord = curr_coord.apply_box_action(action[0])
            path.append(curr_coord)
        return(path)


    def __eq__(self,other):
        if isinstance(other, Coords):
            return self.x==other.x and self.y==other.y
        return False
