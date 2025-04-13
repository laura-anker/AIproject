'''opponent snake is player/player 1, me is the ai/player 2'''
from Entity import Entity

class GameState:
    def __init__(self, edibles_two_player_scene):
        self.opp_head = edibles_two_player_scene.head_1
        self.me_head = edibles_two_player_scene.head_2
        self.opp_tail = edibles_two_player_scene.tail_1
        self.me_tail = edibles_two_player_scene.tail_1
        #positive means going right, negative left
        self.opp_dx = edibles_two_player_scene.dx1
        #positive means going down, negative up
        self.opp_dy = edibles_two_player_scene.dy1
        self.me_dx = edibles_two_player_scene.dx2
        self.me_dy = edibles_two_player_scene.dy2
        self.apple = edibles_two_player_scene.apple
        self.walls = self.get_walls(edibles_two_player_scene.w, edibles_two_player_scene.h, edibles_two_player_scene.director.scale)
        self.w = edibles_two_player_scene.w
        self.h = edibles_two_player_scene.h
        self.scale = edibles_two_player_scene.director.scale
        self.screen = edibles_two_player_scene.director.screen

    def get_walls(self, width, height, scale):
        walls = []
        for i in range(0, width, 10 * scale):
            walls.append(Entity(i, 0, 10 * scale, 10 * scale, (255, 255, 255)))  # top wall
            walls.append(Entity(i, height - 10 * scale, 10 * scale, 10 * scale, (255, 255, 255)))  # bottom wall
        for i in range(0, height, 10 * scale):
            walls.append(Entity(0, i, 10 * scale, 10 * scale, (255, 255, 255)))  # left wall
            walls.append(Entity(width - 10 * scale, i, 10 * scale, 10 * scale, (255, 255, 255)))  # right wall
        return walls

    def get_my_head(self):
        return self.me_head.x, self.me_head.y
    
    def get_opp_head(self):
        return self.opp_head.x, self.opp_head.y

    def get_apple_position(self):
        return self.apple.x, self.apple.y

    def get_my_tail_positions(self):
        return [(segment.x, segment.y) for segment in self.me_tail]
    
    def get_opp_tail_positions(self):
        return [(segment.x, segment.y) for segment in self.opp_tail]

    def get_wall_positions(self):
        return [(wall.x, wall.y) for wall in self.walls]
    
    #returns list of resulting (dx, dy) values for the given agent snake (1  = opp/player, 2 = ai)
    def get_legal_actions(self, agent):
        possibleActions = []
        #for opponent/player snake
        if agent == 1:
        #the snake can legally move any direction except backwards into itself
            # if my snake is not moving on the x-axis (opp_dx == 0) or it is moving right (opp_dx>0)
            # then is can go right
            if self.opp_dx >= 0:
                #RIGHT
                possibleActions.append(((10 *self.scale), 0))
            # if my snake is not moving on the x-axis (opp_dx == 0) (covered above) 
            # or it is moving left (opp_dx<0) then is can go left
            if self.opp_dx < 0:
                #LEFT
                possibleActions.append(((-10 *self.scale), 0))
            # if my snake is not moving on the y-axis (opp_dy == 0) or it is moving down (opp_dy>0)
            # then is can go down
            if self.opp_dy >= 0:
                #DOWN
                possibleActions.append((0, (10 *self.scale)))
            # if my snake is not moving on the y-axis (opp_dy == 0) (covered above) 
            # or it is moving up (opp_dy<0) then is can go up
            if self.opp_dy < 0:
                #UP
                possibleActions.append((0, (-10 *self.scale)))
        if agent == 2:
        #the snake can legally move any direction except backwards into itself
            # if my snake is not moving on the x-axis (opp_dx == 0) or it is moving right (opp_dx>0)
            # then is can go right
            if self.me_dx >= 0:
                #RIGHT
                possibleActions.append(((10 *self.scale), 0))
            # if my snake is not moving on the x-axis (opp_dx == 0) (covered above) 
            # or it is moving left (opp_dx<0) then is can go left
            if self.me_dx < 0:
                #LEFT
                possibleActions.append(((-10 *self.scale), 0))
            # if my snake is not moving on the y-axis (opp_dy == 0) or it is moving down (opp_dy>0)
            # then is can go down
            if self.me_dy >= 0:
                #DOWN
                possibleActions.append((0, (10 *self.scale)))
            # if my snake is not moving on the y-axis (opp_dy == 0) (covered above) 
            # or it is moving up (opp_dy<0) then is can go up
            if self.me_dy < 0:
                #UP
                possibleActions.append((0, (-10 *self.scale)))
        return possibleActions
    
    #checks if ai won
    def isWin(self):
        # This loop iterates through each tail segment in the first snake's tail
        for i in self.opp_tail:
            # This conditional statement checks if the first snake's head has gone out of bounds and if so then it 
            # means the ai has won
            if self.opp_head.x == i.x and self.opp_head.y == i.y or self.opp_head.x < 0 or self.opp_head.x > self.w or self.opp_head.y < 0 or self.opp_head.y > self.h:
                return True
        for i in self.me_tail:
            # This conditional statement checks if the current tail segment and the head of the player snake occupy the
            # same space. If so it means the ai has won
            if self.opp_head.x == i.x and self.opp_head.y == i.y:
                return True
        return False

    #checks if ai lost
    def isLose(self):
        # This loop iterates through each tail segment in the first snake's tail
        for i in self.opp_tail:
            # This conditional statement checks if the current tail segment and the head of the second snake occupy the
            # same space. If so it means the player has won
            if self.me_head.x == i.x and self.me_head.y == i.y:
                return True
        for i in self.me_tail:
            # This conditional statement checks if the ai snake's head has gone out of bounds and if so then it
            # means the player has won
            if self.me_head.x == i.x and self.me_head.y == i.y or self.me_head.x < 0 or self.me_head.x > self.w or self.me_head.y < 0 or self.me_head.y > self.h:
                return True
        return False

    #checks if it's a draw
    def isDraw(self):
        if self.opp_head.x == self.me_head.x and self.opp_head.y == self.me_head.y:
            return True
        return False
    
    #returns resulting state given (dx, dy) action for the given agent snake (1  = opp/player, 2 = ai)
    def generateSuccessor(self, agent, action):
        # Check that successors exist
        if self.isWin() or self.isLose() or self.isDraw(): raise Exception('Can\'t generate a successor of a terminal state.')
        #copy current state
        state = GameState(self)

        #move agent based on action
        if agent == 1:
            state.opp_dx = action[0]
            state.opp_dy = action[1]
        if agent == 2:
            state.me_dx = action[0]
            state.me_dy = action[1]
        #we don't know what the other agent's action will be??

        #check if apple was eaten
            #if so move apple???? - this will be random



