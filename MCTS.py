from UtilTwoSnake import GameState
import random
import math
import time

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

    def run(self, depth, loop_time):
        #for some amount of time do a thing
        # d = depth
        # while d > 0:
        time_to_loop = time.time() + loop_time
        while time.time() < time_to_loop:
            leaf = self.select()
            child = self.expand(leaf)
            result = self.simulate(child)
            #we could skip back propogation if result is a draw? depends how we want to calculate score (traditionally it's just wins/total)
            self.backpropogate(result, child)
        #return best action to take by comparing scores of children of the root and picking action of child with greater score
        children_rankings = {}
        for child in self.root.children:
            ranking = child.totalScore / child.numVisits
            children_rankings[ranking] = child
            print(f"{child.children=}")
            print(f"{child.numVisits=}")
            print(f"{child.totalScore=}")
        print(f"{children_rankings=}")
        return children_rankings[max(children_rankings)].action

    #move down the tree to select a node via some selection protocol, returns selected node
    def select(self):
        #could use UCB1 formula
            # Sure, why not:
            # Recall the formula: UCB1(n) = (U(n)/N(n)) + C * sqrt((log(N(Parent(n)))/(N(n)))
        # I guess we can just compute this for each child then choose the one with
            # the largest UCB1 ranking? Let's just try it like that!
        # OOHHHHHH WAIT THIS IS EASIER THAN I THOUGHT YAYYY NO RECURSION NEEDED
            # I thought I would have to expand children of children of children BUT
            # that's the job of the expand function: is to see if we already
            # expanded this node, if we have then expand a child further down the tree
                # *do we need another select call then? or just choose a child randomly?*
            # so all this method has to do is analyze the root's children, not
            # the children's children the expand call should take care of expanding futher
            # down or not
        # If there are no children, just return the root:
        if self.root.children == None:
            return self.root
        # Otherwise, do all this stuffis
        children_rankings = {}
        for child in self.root.children:
            U = child.totalScore
            N = child.numVisits
            C = 1.41 # 'Agreed' upon value for this scalar is sqrt(2) ~ 1.41, but
                # edit this to get better results, like 1.5 or 1.3
            Parent_N = child.parent.numVisits
            ranking = (U/N) + C * math.sqrt((math.log(Parent_N))/(N))
            children_rankings[ranking] = child
        # Now let's just get the child at the max value in the dictionary
            # and return that!
        # Did I find this shorthand online?! Yes! Yay python being easy to copy...
        highest_child = max(children_rankings)
        return children_rankings[highest_child]

    #add one (or more?) child node(s) with score 0, returns child
    #currently this does the one child thing
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
        # Basically, if we find a endstate here we should just return itself
            # sometimes gameOver isn't set to true, just do it again here
            # I don't want to find out where it's not being set right not...
        if leaf.state.isWin() or leaf.state.isLose() or leaf.state.isDraw():
            leaf.state.gameOver = True
            return leaf
        states = []
        if leaf.children == None:
            leaf.children = []
        else:
            for c in leaf.children:
                states.append(c.state)
        #randomly choose an action
        actions = leaf.state.get_legal_actions(2)
        print(f"{actions=}")
        action = random.choice(actions)
        #randomly generate successor state from action
        state = leaf.state.generateRandomSuccessor(action)
        print(f"{state.gameOver=}")
        print(f"{state.get_legal_actions(2)=}")
        #check that the successor has not already been generated
        bl = True
        while bl == True:
            bl = False
            for s in states:
                if s.is_equal(state):
                    state = leaf.state.generateRandomSuccessor(action)
                    bl = True
        #create, add, and return new node
        newNode = Node(state)
        newNode.parent = leaf
        newNode.action = action
        leaf.children.append(newNode)
        return newNode
        #return one of the children? all of the children?
    
    #simulate new states until termination. do not store them in the tree, returns value representing win/lose/draw
    # We're doing a weird thing choosing a random action here and not just using the other
        # method we have in utiltwosnake to generate random successors but who cares...
        # ...it will work and we can stop thinking about how weird this code is
    def simulate(self, child):
        # If child is end state, don't simulate
            # we do actually want to accumulate wins/losses/draws on these gameover nodes though
            # so keep this in here
        if child.state.gameOver:
            if child.state.isWin():
                return 1
            if child.state.isLose():
                return -1
            return -0.5
        print("not 135ish?")
        # Should have used recursion here but it is what it is...
        #i think this is where the getRandomSuccessor comes in
        potential_actions = child.state.get_legal_actions(1)
        random_action = random.choice(potential_actions)
        newState = child.state.generateRandomSuccessor(random_action)
        while newState.gameOver == False:
            # What exactly is going on here!? lol I may need help but this
                # is what I could think of
            potential_actions = newState.get_legal_actions(1)
            random_action = random.choice(potential_actions)
            # Don't want to get child.state.generateRandomSuccessor every time
                # right? Because we want to traverse down the tree
            newState = newState.generateRandomSuccessor(random_action)
        #we should consider how we actually want to score this but this works for now
        if newState.isWin():
            return 1
        if newState.isLose():
            return -1
        return -0.5

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
