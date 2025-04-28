from UtilTwoSnake import GameState

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

    def run(self, depth, currentGameState):
        #for some amount of time do a thing
        d = depth
        while d > 0:
            leaf = self.select()
            child = self.expand(leaf)
            result = self.simulate(child)
            #we could skip back propogation if result is a draw? depends how we want to calculate score (traditionally it's just wins/total)
            self.backpropogate(result, child)
        #return best action to take

    #move down the tree to select a node via some selection protocol, returns selected node
    def select(self):
        #could use UCB1 formula

    #add one (or more?) child node(s) with score 0, returns child
    #currently this generates all children and makes no selection
    #SEVERAL THINGS TO CONSIDER: 
    # If we expand to multiple children: 
    # - must change run method to accomadate going through list
    # - would take longer
    # - must make sure you can't expand same node twice cause all children will be generated
    # If we expand to one child:
    # - should randomly generate action and successor, maybe make new successor method to randomly generate one given action
    # - should check when expanding so you don't accidentally generate same successor twice
    # - tbh I like this idea better
    def expand(self, leaf):
        if leaf.children == None:
            leaf.children = []
        for a in leaf.get_legal_actions():
            for s in leaf.generateSuccessors(a):
                newNode = Node(s)
                newNode.parent = leaf
                newNode.action = a
                leaf.children.append(newNode)
        #return one of the children? all of the children?
    
    #simulate new states until termination. do not store them in the tree, returns value representing win/lose/draw
    def simulate(self, child):
        #i think this is where the getRandomSuccessor comes in
        newState = child.state.generateRandomSuccessor()
        while newState.gameOver == False:
            newState = child.state.generateRandomSuccessor()
        #we should consider how we actually want to score this but this works for now
        if newState.isWin():
            return 1
        if newState.isLose():
            return -1
        return 0


    #go back up the tree from the child, updating each score using result. 
    # I think just add 1 to all visits and add result to every score?
    def backpropogate(self, result, child):
        node = child
        node.numVisits += 1
        node.totalScore += result
        while node.parent != None:
            node = node.parent
            node.numVisits += 1
            node.totalScore += result