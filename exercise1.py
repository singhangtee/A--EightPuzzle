from cosc343EightPuzzle import EightPuzzle
import time

# Definition of a class named 'Node'
class Node:

    def __init__(self, s, parent=None, g=0, h=0, action=None):
        self.s = s              #State
        self.parent = parent    #Reference to parent node
        self.g = g              #Cost
        self.f = g+h            #Evaluation function
        self.action = action    #Action take from parent
                                #nodes state to this node's state

# Function computing misplaced tiles
def heuristic(s,goal):

    h = 0
    #Walk through all tiles in the current state
    for i in range(len(s)):
        if s[i] != goal[i]:
            h+=1
    return h

start_time = time.time()

puzzle = EightPuzzle(mode='medium')

init_state = puzzle.reset()

goal_state = puzzle.goal()

root_node = Node(s=init_state, parent=None, g=0, h=heuristic(s=init_state, goal=goal_state))
fringe = [root_node]

solution_node = None
while len(fringe)>0:
    current_node = fringe.pop(0)
    current_state = current_node.s
    if(current_state == goal_state):
        solution_node = current_node
        break
    else:
        available_actions = puzzle.actions(s=current_state)
        for a in available_actions:
            next_state = puzzle.step(s=current_state, a=a)
            new_node = Node(s=next_state,
                            parent=current_node,
                            g=current_node.g+1,
                            h=heuristic(s=next_state, goal= goal_state),action=a)
            fringe.append(new_node)
            fringe.sort(key=lambda x: x.f)

if solution_node is None:
    print("Didn't find a solution!!!")
else:

    action_sequence = []

    next_node = solution_node
    while True:
        if next_node == root_node:
            break

        action_sequence.append(next_node.action)
        next_node = next_node.parent
        
    action_sequence.reverse()
    print("Number of moves: %d" % solution_node.g)

elapsed_time = time.time() - start_time
print("Elapsed time: %.1f seconds" % elapsed_time)

puzzle.show(s=init_state, a=action_sequence)

