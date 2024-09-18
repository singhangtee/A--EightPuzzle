from cosc343EightPuzzle import EightPuzzle
import time
import heapq

# Definition of a class named 'Node'
class Node:
    def __init__(self, s, parent=None, g=0, h=0, action=None):
        self.s = s              # State
        self.parent = parent    # Reference to parent node
        self.g = g              # Cost
        self.h = h              # Heuristic
        self.f = g + h          # Evaluation function
        self.action = action    # Action taken to reach this node

    def __lt__(self, other):
        return self.f < other.f

# Function computing Manhattan distance
def heuristic(s, goal):
    h = 0
    for i in range(len(s)):
        if s[i] != 0:  # Ignore the blank tile
            goal_index = goal.index(s[i])
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_index, 3)
            h += abs(current_row - goal_row) + abs(current_col - goal_col)
    return h

start_time = time.time()

puzzle = EightPuzzle(mode='hard')

init_state = puzzle.reset()
goal_state = puzzle.goal()

root_node = Node(s=init_state, parent=None, g=0, h=heuristic(s=init_state, goal=goal_state))
fringe = []
heapq.heappush(fringe, root_node)

explored = set()
explored.add(tuple(init_state))

solution_node = None

while fringe:
    current_node = heapq.heappop(fringe)
    current_state = current_node.s

    if current_state == goal_state:
        solution_node = current_node
        break

    available_actions = puzzle.actions(s=current_state)
    for a in available_actions:
        next_state = puzzle.step(s=current_state, a=a)
        next_state_tuple = tuple(next_state)

        if next_state_tuple not in explored:
            explored.add(next_state_tuple)
            new_node = Node(s=next_state,
                            parent=current_node,
                            g=current_node.g + 1,
                            h=heuristic(s=next_state, goal=goal_state),
                            action=a)
            heapq.heappush(fringe, new_node)

if solution_node is None:
    print("Didn't find a solution!!!")
else:
    action_sequence = []

    next_node = solution_node
    while next_node.parent:
        action_sequence.append(next_node.action)
        next_node = next_node.parent

    action_sequence.reverse()
    print("Number of moves: %d" % solution_node.g)

elapsed_time = time.time() - start_time
print("Elapsed time: %.1f seconds" % elapsed_time)

puzzle.show(s=init_state, a=action_sequence)
