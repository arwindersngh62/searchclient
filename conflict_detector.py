from plan import Plan
## input to the method is : 
# in case of normal conflict : ((plan_a, plan_b), [((0, 6), 3)])
# in case of swap conflict : ((plan_a, plan_b), [((0, 6), 3)#conflicting earlier step of plan 1,((0,6),4)# conflicting later coord of step b])
#  [(<ConflictEnum.SwappingCells: 1>, (3688, 3944), [[((0, 3), 2), ((0, 3), 1)]])]  Something like this?
#              Enum                     p1     p2       p1.coord        p2.coord
# there is no usefulness of multiple conflicts returning because 
# the whole thing is based on the fact that the detected conflict is the first conflict from the perspective of time coords in all the curent plans
plan_a = Plan()
plan_a.path = [ ((1,5), 1), ((0,5), 2),((0,6),3), ((0,7), 4), ((0,8), 5),((0,9), 6), ((1,9), 7), ((2,9), 8)]
plan_a.priority = 0
plan_b = Plan()
plan_b.path = [ ((1,8), 1), ((0,8), 2), ((0, 7), 3),((0,6), 4), ((0,5), 5), ((1,5), 6)]
#plan_b.path = [ ((1,7), 1), ((0,7), 2), ((0, 6), 3),((0,5), 4), ((0,4), 5), ((1,4), 6)]
plan_b.priority = 0
conflict = ((plan_a, plan_b), [((0, 6), 3),((0,6),4)])
#conflict = ((plan_a, plan_b), [((0, 6), 3)])
#conflict
def conflict_solver(conflict):
    plan_a = conflict[0][0]
    plan_b = conflict[0][1]
    if plan_a.priority< plan_b.priority:
        waiting = plan_b
        moving = plan_a
    else:
        waiting = plan_b
        moving = plan_a
        exchanged = True
    print(conflict[1])
    if len(conflict[1])>1:
        print('here')
        if exchanged:
            conflict_index_a = waiting.path.index(conflict[1][1])
            conflict_index_b = moving.path.index(conflict[1][0])
            i = conflict_index_b-1
            j = conflict_index_a+1
        else:
            conflict_index_a = waiting.path.index(conflict[1][0])
            conflict_index_b = moving.path.index(conflict[1][1])
            i = conflict_index_a-1
            j = conflict_index_b+1
    else:
        #        conflict_index_a = waiting.path.index(conflict[1][0])
        conflict_index = waiting.path.index(conflict[1][0])
        i = conflict_index-1
        j = conflict_index+1
        
    while i>0 and j<len(moving.path):
        if waiting.path[i] == moving.path[j]:
            i=i-1
            j=j+1
        else:
            break
    wait_from = waiting.path[i-1][1]
    wait_till = moving.path[j][1]
    wait_ops = wait_till - wait_from
    prev = waiting.path[:wait_from]
    next = waiting.path[wait_from:]
    waiting_oops = []
    print(prev)
    print(next)
    print(wait_ops)

    waiting_oops = [prev[-1] for i in range(wait_ops)]
    new_plan = prev + waiting_oops + next
    start_time = new_plan[0][1]
    for i in range(len(new_plan)):
        if (new_plan[i][1] == i+start_time):
            continue
        else:
            new_plan[i] = (new_plan[i][0],i+start_time)
        
    return (moving.path,new_plan)

print(conflict_solver(conflict))


