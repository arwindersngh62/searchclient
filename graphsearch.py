import memory
import time
import sys

from action import Action
globals().update(Action.__members__)

start_time = time.perf_counter()

def search(initial_state, frontier):

                output_fixed_solution = False

                if output_fixed_solution:
                                # Part 1: 
                                # The agents will perform the sequence of actions returned by this method.
                                # Try to solve a few levels such as SAD1 and SAD2 by hand and entering them below:

                                return [
                                                [PullEN],
                                                [PullEE],
                                                [PullEE],
                                                [PullEE],
                                                [PullEE],
                                                
                                                [PushWS],
                                                [PushSE]
                                                
                                ]

                else:
                                # Part 2: 
                                # Now try to implement the Graph-Search algorithm from R&N figure 3.7
                                # In the case of "failure to find a solution" you should return None.
                                # Some useful methods on the state class which you will need to use are:
                                # state.is_goal_state() - Returns true if the state is a goal state.
                                # state.extract_plan() - Returns the list of actions used to reach this state.
                                # state.get_expanded_states() - Returns a list containing the states reachable from the current state.
                                # You should also take a look at frontier.py to see which methods the Frontier interface exposes

                                iterations = 0

                                frontier.add(initial_state)
                                #print('#'+str(initial_state))
                                explored = set()

                                while True:
                                                #print('#'+str(iterations))
                                                iterations += 1
                                                if iterations % 1000 == 0:
                                                                print_search_status(explored, frontier)

                                                if memory.get_usage() > memory.max_usage:
                                                                print_search_status(explored, frontier)
                                                                print('Maximum memory usage exceeded.', file=sys.stderr, flush=True)
                                                                return None
                                                #frontier.pop()

                                                if frontier.is_empty():
                                                               # print("frontier empty")
                                                                return None
                                                else:
                                                                #print("#here")
                                                                curr_state = frontier.pop()
                                                                
                                                                explored.add(curr_state)
                                                                new_states = curr_state.get_expanded_states()
                                                                ##print(str(curr_state.boxes))
                                                                if curr_state.is_goal_state():
                                                                                return (curr_state.extract_plan())
                                                                else:          
                                                                                for state in new_states:
                                                                                                if state in explored:
                                                                                                            pass
                                                                                                else:
                                                                                                            if frontier.contains(state):
                                                                                                                        pass
                                                                                                            else:
                                                                                                                        frontier.add(state)
                                                                                                
                                                                                
                                                # Your code here...

def print_search_status(explored, frontier):
                status_template = '#Expanded: {:8,}, #Frontier: {:8,}, #Generated: {:8,}, Time: {:3.3f} s\n[Alloc: {:4.2f} MB, MaxAlloc: {:4.2f} MB]'
                elapsed_time = time.perf_counter() - start_time
                print(status_template.format(len(explored), frontier.size(), len(explored) + frontier.size(), elapsed_time, memory.get_usage(), memory.max_usage), file=sys.stderr, flush=True)
