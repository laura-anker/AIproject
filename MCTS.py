class Node:
    def __init__(self, gameState):
        self.state = gameState
        #list of children of the node
        self.children = None
        self.numVisits = 0
        self.totalScore = 0
        #action to get to this state
        self.action = None
        #parent of this node for travelling up the tree
        self.parent = None

class Mcts:
    def __init__(self, gameState):
        self.root = Node(gameState)
'''
    def run():
        #for some amount of time do a thing
        #return best action to take

    def select():

    def expand():
    
    def simulate():
        #i think this is where the getRandomSuccessor comes in

    def backpropogate():'''