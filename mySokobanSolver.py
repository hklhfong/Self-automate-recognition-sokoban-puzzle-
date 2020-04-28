
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

# External library
import math
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(10107321, 'Ho Fong', 'Law'), (10031014, 'Kiki', 'Mutiara')]

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
    X, Y = zip(*warehouse.walls)
    x_size, y_size = 1+max(X), 1+max(Y)
    coner_List = []
    coner = []
    targets_List = []
    str_puzzle = [[" "] * x_size for y in range(y_size)]
    first_row_wall = 0
    first_col_wall = 0
    left_walls = right_walls = top_walls =  bottom_walls = []

    for (x, y) in warehouse.walls:
        str_puzzle[y][x] = "#"

# find the outside and inside
    for y in range(warehouse.nrows):
        first_col_wall = True
        for x in range(warehouse.ncols):
            if (x, y) in warehouse.walls and first_col_wall:
                first_col_wall = False
                left_walls.append([x, y])
            if x == warehouse.ncols - 1:
                temp_col = x
                # for col in range(warehouse.ncols):
                while True:
                    if (temp_col, y) in warehouse.walls:
                        break
                    temp_col = temp_col - 1
                right_walls.append([temp_col, y])

    for x in range(warehouse.ncols):
        first_row_wall = True
        for y in range(warehouse.nrows):
            if (x, y) in warehouse.walls and first_row_wall:
                first_row_wall = False
                top_walls.append([x, y])
            if y == warehouse.nrows - 1:
                temp_row = y
                # for row in range(warehouse.nrows):
                while True:
                    if (x, temp_row) in warehouse.walls:
                        break
                    temp_row = temp_row - 1
                bottom_walls.append([x, temp_row])

# rule number 1
    for y in range(warehouse.nrows):
        for x in range(warehouse.ncols):
            if not (x, y) in warehouse.walls:
                if (x, y) in warehouse.targets:
                    targets_List.append((x, y))
                    continue
                if (x-1, y) in warehouse.walls:
                    if (x, y-1) in warehouse.walls:
                        coner.append((x, y))
                        continue
                    if (x, y+1) in warehouse.walls:
                        coner.append((x, y))
                        continue

                if (x+1, y) in warehouse.walls:
                    if (x, y-1) in warehouse.walls:
                        coner.append((x, y))
                        continue
                    if (x, y+1) in warehouse.walls:
                        coner.append((x, y))
                        continue

                if (x, y-1) in warehouse.walls:
                    if (x-1, y) in warehouse.walls:
                        coner.append((x, y))
                        continue
                    if (x+1, y) in warehouse.walls:
                        coner.append((x, y))
                        continue

                if (x, y+1) in warehouse.walls:
                    if (x-1, y) in warehouse.walls:
                        coner.append((x, y))
                        continue
                    if (x+1, y) in warehouse.walls:
                        coner.append((x, y))
                        continue


# determent outside or inside the wall
    for (x, y) in coner:
        for (left_col, left_row) in left_walls:
            if x > left_col and left_row == y:
                for(right_col, right_row) in right_walls:
                    if x < right_col and right_row == y:
                        for (top_col, top_row) in top_walls:
                            if y > top_row and top_col == x:
                                for (bottom_col, bottom_row) in bottom_walls:
                                    if y < bottom_row and bottom_col == x:
                                        coner_List.append((x, y))
# rule number 2
    xSymbolList = coner_List
    for (x, y) in coner_List:
        n = 1
        while (x+n, y) not in warehouse.walls:

            if (x+n, y+1) not in warehouse.walls and (x+n, y-1) not in warehouse.walls:
                n = 0
                tempXSymbolList = []
            if (x+n, y) in warehouse.targets and (x+n, y) not in coner_List:
                n = 0
                tempXSymbolList = []

            if (x+n, y) in xSymbolList:
                for temp in tempXSymbolList:

                    xSymbolList.append(temp)
                n = 0

            if n == 0:
                break
            tempXSymbolList.append((x+n, y))
            n = n+1
        n = 1
        while (x, y+n) not in warehouse.walls:
            # print ('x,y+n = '+ str((x,y+n)))
            if (x+1, y+n) not in warehouse.walls and (x-1, y+n) not in warehouse.walls:
                n = 0
                tempXSymbolList = []
            if (x, y+n) in warehouse.targets and (x, y+n) not in coner_List:
                n = 0
                tempXSymbolList = []
            if (x, y+n) in xSymbolList:
                for temp in tempXSymbolList:
                    xSymbolList.append(temp)
                n = 0

            if n == 0:
                break
            tempXSymbolList.append((x, y+n))
            n = n+1

# draw the X
    for (x, y) in xSymbolList:
        str_puzzle[y][x] = "X"

    return "\n".join(["".join(line) for line in str_puzzle])

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
    first_row_wall, first_column_wall = None, None
    for row, line in enumerate(lines):
        brick_column = line.find('#')
        if brick_column >= 0:
            if first_row_wall is None:
                first_row_wall = row  # found first row with a brick
            if first_column_wall is None:
                first_column_wall = brick_column
            else:
                first_column_wall = min(first_column_wall, brick_column)
    if first_column_wall is None:
        raise ValueError('Warehouse with no walls!')
    # compute the canonical representation
    # keep only the lines that contain walls
    canonical_lines = [line[first_column_wall:]
                       for line in lines[first_row_wall:] if line.find('#') >= 0]
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

    def __init__(self, initial=None, allow_taboo_push=None, macro=None,
                 push_costs=None):
        # print('This is the initial state:\n' + self.initial)
        self.initial = initial.__str__()
        self.push_costs = push_costs
        self.goal = initial.copy(boxes=initial.targets).__str__()
        self.ListofLocation = initial.boxes
        if allow_taboo_push:
            self.allow_taboo_push = allow_taboo_push
        else:
            self.allow_taboo_push = True
        if macro:
            self.macro = macro
        else:
            self.macro = False

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        new_wh = sokoban.Warehouse()
        new_wh.extract_locations(state.split(sep="\n"))
        list_of_actions = []
        for direction in (UP, RIGHT, DOWN, LEFT):
            if self.macro:
                for box in new_wh.boxes:
                    newLoc = direction.go(box)
                    workerLoc = (box[1] + -1 * direction.stack[1], box[0] +
                                 -1 * direction.stack[0])
                    if can_go_there(new_wh, workerLoc):
                        if newLoc not in new_wh.walls and newLoc not in new_wh.boxes:
                            if self.allow_taboo_push:
                                list_of_actions.append((box, direction))
                            else:
                                if newLoc not in read_taboo_cells(taboo_cells
                                                                  (new_wh)):
                                    list_of_actions.append((box, direction))
            else:
                location_one = location_two = new_wh.worker
                location_one = direction.go(location_one)
                location_two = direction.go(location_one)
                if location_one in new_wh.boxes:
                    if location_two not in new_wh.boxes and location_two not in new_wh.walls:
                        if self.allow_taboo_push:
                            list_of_actions.append(direction)
                        else:
                            if location_two not in read_taboo_cells(taboo_cells
                                                                    (new_wh)):
                                list_of_actions.append(direction)
                if location_one not in new_wh.boxes and location_one not in new_wh.walls:
                    list_of_actions.append(direction)
        return list_of_actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_wh = sokoban.Warehouse()
        new_wh.extract_locations(state.split(sep="\n"))
        if self.macro:
            original_location = action[0]
            if original_location in new_wh.boxes:
                # remove original box position
                new_wh.boxes.remove(original_location)
                # move box to new position
                new_wh.worker = original_location
                new_location = action[1].go(original_location)
                new_wh.boxes.append(new_location)
        else:
            location_one = location_two = new_wh.worker
            location_one = action.go(location_one)
            location_two = action.go(location_one)
            # check locations is valid or not
            if location_one in new_wh.boxes:
                if location_two not in new_wh.boxes and location_two not in new_wh.walls:
                    new_wh.boxes.remove(location_one)
                    new_wh.boxes.append(location_two)
            new_wh.worker = location_one
        return new_wh.__str__()

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        new_wh1 = sokoban.Warehouse()
        new_wh1.extract_locations(state.split(sep="\n"))
        new_wh2 = sokoban.Warehouse()
        new_wh2.extract_locations(self.goal.split(sep="\n"))
        return set(new_wh1.boxes) == set(new_wh2.targets)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        new_wh2 = sokoban.Warehouse()
        new_wh2.extract_locations(state2.split(sep="\n"))
        if self.push_costs == None:
            # normal situation
            return c + 1
        else:
            # weight element move
            for i in range(len(self.ListofLocation)):
                if self.ListofLocation[i] not in new_wh2.boxes:
                    cost = self.push_costs[i]
                    for (x, y) in new_wh2.boxes:
                        if (x, y) not in self.ListofLocation:
                            self.ListofLocation[i] = (x, y)
                            return c + cost
            else:
                return c + 1

    def h(self, n):
        heur = 0
        # print ('h function:n.state : \n'+ n.state+'\n')
        new_wh = sokoban.Warehouse()
        new_wh.extract_locations(n.state.split(sep="\n"))
        for box in new_wh.boxes:
                # find the nearest target
            closest_target = new_wh.targets[0]
            for target in new_wh.targets:
                if(manhattan_distance(target, box) < manhattan_distance(closest_target, box)):
                    closest_target = target

                 # updateHeuristic
            heur = heur + manhattan_distance(closest_target, box)

        return heur

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



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
    location_one = location_two = warehouse.worker
    for step in action_seq:
        if step == 'Left':
            location_one = LEFT.go(location_one)
            location_two = LEFT.go(location_one)
        elif step == 'Right':
            location_one = RIGHT.go(location_one)
            location_two = RIGHT.go(location_one)
        elif step == 'Up':
            location_one = UP.go(location_one)
            location_two = UP.go(location_one)
        elif step == 'Down':
            location_one = DOWN.go(location_one)
            location_two = DOWN.go(location_one)
        # check if step legal
        if location_one in warehouse.walls:
            return 'Impossible'
        if location_one in warehouse.boxes:
            if location_two in warehouse.boxes or location_two in warehouse.walls:
                return 'Impossible'
            warehouse.boxes.remove(location_one)
            warehouse.boxes.append(location_two)
        warehouse.worker = location_one
    return warehouse.__str__()


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
    puzzle = SokobanPuzzle(warehouse, True, False)
    puzzleGoalState = warehouse.copy()
    if (set(puzzleGoalState.boxes) == set(puzzleGoalState.targets)):
        return []
    puzzleSolution = search.astar_graph_search(puzzle)
    step_move = []
    if (puzzleSolution is None):
        return 'Impossible'
    else:
        for node in puzzleSolution.path():
            step_move.append(node.action.__str__())
        action_seq = step_move[1:]
        if check_elem_action_seq(warehouse, action_seq) == 'Impossible':
            return 'Impossible'
        else:
            return action_seq


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.

    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    destination = (dst[1], dst[0])
    path = search.astar_graph_search(
        TempSokuban(warehouse.worker, destination, warehouse))
    if path is None:
        return False
    else:
        return True


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

    puzzle = SokobanPuzzle(warehouse, True, True)
    puzzleGoalState = warehouse.copy()
    if (puzzleGoalState.boxes == puzzleGoalState.targets):
        return []
    puzzleSolution = search.astar_graph_search(puzzle)
    step_move = []
    if (puzzleSolution is None):
        return 'Impossible'
    else:
        for node in puzzleSolution.path():
            action = node.action
            if action is None:
                continue
            step_move.append(
                ((action[0][1], action[0][0]), action[1].__str__()))
        action_seq = step_move[:]
        return action_seq


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

    puzzle = SokobanPuzzle(warehouse, True, False, push_costs)
    puzzleGoalState = warehouse.copy()
    if (puzzleGoalState.boxes == puzzleGoalState.targets):
        return []
    puzzleSolution = search.astar_graph_search(puzzle)
    step_move = []
    if (puzzleSolution is None):
        return 'Impossible'
    else:
        for node in puzzleSolution.path():
            step_move.append(node.action.__str__())
        action_seq = step_move[1:]
        if check_elem_action_seq(warehouse, action_seq) == 'Impossible':
            return 'Impossible'
        else:
            return action_seq


class Way:

    def __init__(self, name, stack):

        self.name = name
        self.stack = stack
        
    def go(self, position):

        return (position[0] + self.stack[0], position[1] + self.stack[1])

    def stack(self):

        return self.stack

    def __str__(self):

        return str(self.name)

  


UP = Way("Up", (0, -1))
RIGHT = Way("Right", (1, 0))
DOWN = Way("Down", (0, 1))
LEFT = Way("Left", (-1, 0))


class TempSokuban(search.Problem):

    def __init__(self, initial, goal, warehouse):
        '''
        Assign the passed values

        @param
            initial: the initial value of the worker
            warehouse: the warehouse object
            goal: the destination
        '''
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse

    def actions(self, state):
        listOfActions = []
        for direct in (UP, RIGHT, DOWN, LEFT):
            nextStep = direct.go(state)
            if nextStep not in self.warehouse.walls and nextStep not in self.warehouse.boxes:
                listOfActions.append(direct)
        return listOfActions

    def result(self, state, step):
        position = state
        position = step.go(position)
        return position

    def h(self, n):
        state = n.state
        curGoal = self.goal
        return math.sqrt((state[0]-curGoal[0])**2+(state[1]-curGoal[1])**2)


def manhattan_distance (loca_a, loca_b):
    # return xy distance between two points
    return abs((loca_a[0] - loca_b[0])) + abs((loca_a[1] - loca_b[1]))
