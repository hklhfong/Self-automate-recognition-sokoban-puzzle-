
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and results in a fail for the test of your code.
This is not negotiable! 


'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
import random, time
import direction
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10107321, 'Ho Fong', 'Law'), (1234568, 'Kiki', 'Mutiara'), (1234569, 'Vincentius', 'Herdian Sungkono') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    xSymbolList = []
    strPuzzle = [[" "] * x_size for y in range(y_size)]
    wall_counter = 0
    
    
    for (x,y) in warehouse.walls:
            strPuzzle[y][x] = "#"
            
    for x in range(warehouse.nrows):
        for y in range(warehouse.ncols):
            if (x,y) in warehouse.walls:
                wall_counter = (wall_counter + 1) % 2
            
            
            if not (x,y) in warehouse.walls and not (x,y) in warehouse.targets:
                if (x-1,y) in warehouse.walls or (x-1,y) in xSymbolList:
                    if (x,y-1) in warehouse.walls or (x,y-1) in xSymbolList:
                        if wall_counter:
                            xSymbolList.append([x,y])
                            continue
                    if (x,y+1) in warehouse.walls or (x,y+1) in xSymbolList:
                        if wall_counter:
                            xSymbolList.append([x,y])  
                            continue
                if (x+1,y) in warehouse.walls or (x+1,y) in xSymbolList:
                    if (x,y-1) in warehouse.walls or (x,y-1) in xSymbolList:
                        if wall_counter:    
                            xSymbolList.append([x,y]) 
                            continue
                    if (x,y+1) in warehouse.walls or (x,y+1) in xSymbolList:
                        if wall_counter:
                            xSymbolList.append([x,y])  
                            continue
                    
    for (x,y) in xSymbolList:
            strPuzzle[y][x] = "X"
    
    return "\n".join(["".join(line) for line in strPuzzle])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def read_taboo_cells(taboo_cells_str):
    '''
    Parameters
    ----------
    taboo_cells_str : string
        A warehouse string version onyl with taboo and walls.

    Raises
    ------
    ValueError
        When wall is empty raise error.

    Returns
    -------
    list
        A list that represent taboo position exmaple :[[x,y]...[xn,yn]].

    '''
    lines = taboo_cells_str.split(sep='\n')    
    first_row_brick, first_column_brick = None, None
    for row, line in enumerate(lines):
        brick_column = line.find('#')
        if brick_column>=0: 
            if  first_row_brick is None:
                first_row_brick = row # found first row with a brick
            if first_column_brick is None:
                first_column_brick = brick_column
            else:
                first_column_brick = min(first_column_brick, brick_column)
    if first_row_brick is None:
        raise ValueError('Warehouse with no walls!')
    # compute the canonical representation
    # keep only the lines that contain walls
    canonical_lines = [line[first_column_brick:] 
                       for line in lines[first_row_brick:] if line.find('#')>=0]
    return list(sokoban.find_2D_iterator(canonical_lines, "X"))    
              

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, initial=None, goal=None, allow_taboo_push=False, macro=False):
     
    
        
        if goal is None:
            self.goal = initial.copy()
            self.goal.boxes = self.goal.targets
        else:
            self.goal = goal #assumen it represent warehouse class
        self.initial = initial #assumen it also represent warehouse class
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        listOfActions = []
        # transition_cost = 1

        for direct in (UP, RIGHT, DOWN, LEFT):
            new_position = direct.go(list(state.worker))
            
            if new_position[0] < 0 or new_position[0] >= state.ncols - 1:
                continue
            if new_position[1] < 0 or new_position[1] >= state.nrows - 1:
                continue
            if new_position in state.walls:
                continue
                            

            if new_position in state.boxes:
                new_box_position = direct.go(new_position)
                
                if new_box_position[0] < 0 or new_box_position[0] >= state.ncols - 1:
                    continue
                if new_box_position[1] < 0 or new_box_position[1] >= state.nrows - 1:
                    continue
                if new_position in state.walls:
                    continue
                if new_box_position in state.boxes:
                    continue
                if not state.allow_taboo_push:
                    if new_box_position in read_taboo_cells(taboo_cells(state)):
                        continue

                # new_state = state.copy(tuple(new_position),new_box_position)
                listOfActions.append(direct.__str__())

        return listOfActions
    
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
       
        str_warehouse = check_elem_action_seq(state, action)
            
        if str_warehouse == 'Impossible':
            return str_warehouse
        
        new_warehouse = sokoban.Warehouse.from_string(str_warehouse)

        return new_warehouse

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def h(self, n):
     	"""
     	"""
     	heur = 0
     	for box in n.state.boxes:
    		#Find closest target
            closest_target = n.state.targets[0]
            for target in n.state.targets:
                if(mDist(target, box) < mDist(closest_target, box)):
                    closest_targetet = target
    				
    		#updateHeuristic
            heur = heur + mDist(closest_target, box)              
    
     	return heur
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def mDist(loca_a, loca_b):

    return abs((loca_a[0] - loca_b[0])) + abs((loca_a[1] - loca_b[1]))



def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    vaild = True
    for step in action_seq:
        x = warehouse.worker[0]
        y = warehouse.worker[1]
        if step == 'Left':
            if [x-1,y] in warehouse.boxes:
                if [x-2,y] in warehouse.boxes:
                    vaild = False
                    break
            elif [x-1,y] in warehouse.walls:
                vaild = False
                break
            else:
                x = x-1
        if step == 'Right':
            if [x+1,y] in warehouse.boxes:
                if [x+2,y] in warehouse.boxes:
                    vaild = False
                    break
            elif [x+1,y] in warehouse.walls:
                vaild = False
                break
            else:
                x = x+1
        if step == 'Up':
            if [x,y-1] in warehouse.boxes:
                if [x,y-2] in warehouse.boxes:
                    vaild = False
                    break
            elif [x,y-1] in warehouse.walls:
                vaild = False
                break
            else:
                y = y-1
        if step == 'Down':
            if [x,y+1] in warehouse.boxes:
                if [x,y+2] in warehouse.boxes:
                    vaild = False
                    break
            elif [x,y+1] in warehouse.walls:
                vaild = False
                break
            else:
                y = y-2
    if vaild:
        return warehouse.__str__()
    else:
        return "Impossible"
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

    # t0 = time.time
    # sol_ts = search.astar_graph_search(warehouse)  # graph search version
    # t1 = time.time()
    # print ('BFS Solver took {:.6f} seconds'.format(t1-t0))
    # if sol_ts == None:
    #     return 'Impossible'
    # else:
    #     return sol_ts.path()
    
    elementary_actions = []

    ##Load macro actions to execute from solve_sokoban_macro
    ##Currently using test data
    macro_actions = solve_sokoban_macro(warehouse)
#    macro_actions = [((3, 6), 'Down'), ((3, 5), 'Down'), ((3, 4), 'Down')]

    print("Initial State:")
    print(warehouse)

    for macro_action in macro_actions: #format is ((r, c), 'Direction')
        #macro action is in ((r, c), 'Direction')
        #warehouse.objects are in (x, y)
        #Calculate the position the worker must be in to move the box
        move_to = (macro_action[0][1], macro_action[0][0])
        
        if macro_action[1] == 'Left':
            move_to = (move_to[0]+1, move_to[1])
        elif macro_action[1] == 'Right':
            move_to = (move_to[0]-1, move_to[1])
        elif macro_action[1] == 'Up':
            move_to = (move_to[0], move_to[1]+1)
        elif macro_action[1] == 'Down':
            move_to = (move_to[0], move_to[1]-1)
            
        #Create SokobanPuzzle object and set goal
        sp = SokobanPuzzle(warehouse, goal = move_to)
        if warehouse.worker == move_to:
            #move worker in desired direction
            warehouse = check_elem_action_seq(warehouse, [macro_action[1]])
        else:
            #move worker to desired location
            sol = search.astar_graph_search(sp)    

            #move worker in desired direction
            warehouse = check_elem_action_seq(sol.state, [macro_action[1]])
            #update list of required elemtary actions
            elementary_actions.extend(sp.return_solution(sol))

        #update list of required elemtary actions
        elementary_actions.append(macro_action[1])

        print("\nafter:" + str(macro_action))
        print(warehouse)
        print("\nElementary Actions Executed:")
        print(elementary_actions)


    print("\nFinal State:")
    print(warehouse)
    print("\nElementary Actions Required:")
    print(elementary_actions)
    
    return elementary_actions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    frontier = set()
    explored = set()
    frontier.add(warehouse.worker)

    while frontier:
        curr_position = frontier.pop()
        if curr_position == (dst[1],dst[0]):
            return True
        explored.add(curr_position)
        
        for direct in (UP, RIGHT, DOWN, LEFT):
            new_position = direct.go(list(warehouse.worker))
            
            if (new_position not in frontier and 
                new_position not in explored and
                new_position not in warehouse.walls and 
                new_position not in warehouse.boxes):
                frontier.add(new_position)
    return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    if warehouse.targets == warehouse.boxes:
        return []
    
    # sokoban_macro = SokobanMacro(warehouse)
    
    results = search.astar_graph_search(warehouse)
    if results == None:
        return ['Impossible']
    path = results.path()
    solution = []
    for node in path:
        solution.append(node.action)
    solution.remove(None)   
    #convert (x,y) to (r,c)
    macro_rc = []
    for action in solution:
        macro_rc.append(((action[0][1], action[0][0]), action[1]))
    
    return macro_rc


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

UP = direction.Way("Up", (0, -1))
RIGHT = direction.Way("Right", (1, 0))
DOWN = direction.Way("Down", (0, 1))
LEFT = direction.Way("left", (-1, 0))