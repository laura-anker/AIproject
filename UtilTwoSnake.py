'''opponent snake is player/player 1, me is the ai/player 2'''
from Entity import Entity
from OppSnakeUtil import Opp_Snake
from MeSnakeUtil import Me_Snake
import random

class GameState:
    def __init__(self, edibles_two_player_scene):
        # Store this for deep copying
        self.edibles_two_player_scene = edibles_two_player_scene
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
        self.director = edibles_two_player_scene.director
        self.gameOver = False

    # Just a nice function to have
    def print(self):
        print(f"""
        === Snake Positions & Directions ===
                    Format: dx, dy
        Opponent:
        Head: {self.opp_head.x}, {self.opp_head.y}
        Tail: NOT IMPLEMENTED
        Direction: {self.opp_dx}, {self.opp_dy}

        Me:
        Head: {self.me_head.x, self.me_head.y}
        Tail: NOT IMPLEMENTED
        Direction: {self.me_dx}, {self.me_dy}

        Apple Position: {self.apple.x}, {self.apple.y}
        """)
    
    # DON'T USE THE self.edibles_two_player_scene VARIABLE (I THINK?)
        # Basically, we only need the information inside gamestate to simulate,
        # why make it hard for us and copy that information to another place when we don't have to,
        # so I didn't implement the updating of that when copying at all.
        # One can change that here and when generating successors if one needs to
    def deep_copy(self):
        copied_game_state = GameState(self.edibles_two_player_scene)
        copied_game_state.edibles_two_player_scene = self.edibles_two_player_scene
        copied_game_state.opp_head = self.opp_head
        copied_game_state.me_head = self.me_head
        copied_game_state.opp_tail = self.opp_tail
        copied_game_state.me_tail = self.me_tail
        copied_game_state.opp_dx = self.opp_dx
        copied_game_state.opp_dy = self.opp_dy
        copied_game_state.me_dx = self.me_dx
        copied_game_state.me_dy = self.me_dy
        copied_game_state.apple = self.apple
        copied_game_state.walls = self.walls
        copied_game_state.w = self.w
        copied_game_state.h = self.h
        copied_game_state.scale = self.scale
        copied_game_state.screen = self.screen
        copied_game_state.director = self.director
        copied_game_state.gameOver = self.gameOver
        return copied_game_state
    
    def is_equal(self, other):
        if (self.opp_head != other.opp_head):
            return False
        if (self.me_head != other.me_head):
            return False
        if (self.me_tail != other.me_tail):
            return False
        if (self.opp_tail != other.opp_tail):
            return False
        if (self.apple != other.apple):
            return False
        if (self.opp_dx != other.opp_dx):
            return False
        if (self.opp_dy != other.opp_dy):
            return False
        if (self.me_dx != other.me_dx):
            return False
        if (self.me_dy != other.me_dy):
            return False
        return True

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
                #possibleActions.append(((10 *self.scale), 0))
                possibleActions.append("right")
            # if my snake is not moving on the x-axis (opp_dx == 0) (covered above) 
            # or it is moving left (opp_dx<0) then is can go left
            if self.opp_dx < 0:
                #LEFT
                #possibleActions.append(((-10 *self.scale), 0))
                possibleActions.append("left")
            # if my snake is not moving on the y-axis (opp_dy == 0) or it is moving down (opp_dy>0)
            # then is can go down
            if self.opp_dy >= 0:
                #DOWN
                #possibleActions.append((0, (10 *self.scale)))
                possibleActions.append("down")
            # if my snake is not moving on the y-axis (opp_dy == 0) (covered above) 
            # or it is moving up (opp_dy<0) then is can go up
            if self.opp_dy < 0:
                #UP
                #possibleActions.append((0, (-10 *self.scale)))
                possibleActions.append("up")
        if agent == 2:
        #the snake can legally move any direction except backwards into itself
            # if my snake is not moving on the x-axis (opp_dx == 0) or it is moving right (opp_dx>0)
            # then is can go right
            if self.me_dx >= 0:
                #RIGHT
                #possibleActions.append(((10 *self.scale), 0))
                possibleActions.append("right")
            # if my snake is not moving on the x-axis (opp_dx == 0) (covered above) 
            # or it is moving left (opp_dx<0) then is can go left
            if self.me_dx < 0:
                #LEFT
                #possibleActions.append(((-10 *self.scale), 0))
                possibleActions.append("left")
            # if my snake is not moving on the y-axis (opp_dy == 0) or it is moving down (opp_dy>0)
            # then is can go down
            if self.me_dy >= 0:
                #DOWN
                #possibleActions.append((0, (10 *self.scale)))
                possibleActions.append("down")
            # if my snake is not moving on the y-axis (opp_dy == 0) (covered above) 
            # or it is moving up (opp_dy<0) then is can go up
            if self.me_dy < 0:
                #UP
                #possibleActions.append((0, (-10 *self.scale)))
                possibleActions.append("up")
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
    
    # returns an action
    def monte_carlo_tree_search(state):
        # tree ‹ NODE(state)
        # while Is-TIME-REMAINING) do
            # leaf ‹ SELECT(tree)
            # child ‹ ExPaND(leaf)
            # result < SIMULATE(child)
            # BACK-PROPAGATE(result, child)
        # return the move in ACTIONS(state) whose node has highest number of playouts
        return
    
    #checks if it's a draw
    def isDraw(self):
        if self.opp_head.x == self.me_head.x and self.opp_head.y == self.me_head.y:
            return True
        return False
    
    # Potentially two ways to implement this: create a new gamestate and snakemove class instance
    # and just use htose or re-implement the logic, let's try the first one first
    # DON'T USE THE self.edibles_two_player_scene VARIABLE (I THINK?)
        # Basically, we only need the information inside gamestate to simulate,
        # why make it hard for us and copy that information to another place when we don't have to,
        # so I didn't implement the updating of that when copying at all
    #returns resulting state given (dx, dy) action for the given agent snake (1  = opp/player, 2 = ai)
    def generateSuccessors(self):
        # Check that successors exist
        if self.isWin() or self.isLose() or self.isDraw(): raise Exception('Can\'t generate a successor of a terminal state.')
        # *hard* copy current state
        state = self.deep_copy()
        # make snake class instances to hold both snakes
        snake_me = Me_Snake(state)
        snake_opp = Opp_Snake(state)
        # List storing all possible successor states
        potential_successors = []

        # Have agents make one random move
        ai_potential_moves = self.get_legal_actions(2)
        player_potential_moves = self.get_legal_actions(1)
        # Iterate through, generating a next state for each potential move for each agent
        # (Any combination of either agent's move)
        for move_me in ai_potential_moves:
            for move_opp in player_potential_moves:
                # Have a fresh copy of our snkae and game state
                potential_snake_me_state = snake_me.deep_copy()
                potential_snake_opp_state = snake_opp.deep_copy()
                potential_game_state = state.deep_copy()
                # Update a hard copied snake, update a hard copied gamestate in that snake
                potential_snake_me_state.make_move(move_me)
                potential_snake_opp_state.make_move(move_opp)
                potential_game_state.me_dx = potential_snake_me_state.dx
                potential_game_state.me_dy = potential_snake_me_state.dy
                potential_game_state.opp_dx = potential_snake_opp_state.dx
                potential_game_state.opp_dy = potential_snake_opp_state.dy
                # Okay, so above we edited the snake's directions, now we have
                # to move the snakes forward one time step
                potential_game_state.step()
                # Check if apple was eaten, if it was replace it using the game logic found in
                # ediblestwoplayer in our state variable above so next time it's
                # copied, it's copied with the new apple, and add one to the length of
                # the snake that ate it
                self.did_eat()
                # Check if the game ended. If so, return a state that displays that.
                if self.isWin() or self.isDraw() or self.isLose():
                    self.gameOver = True
                # add the generated potential state to potential_successors
                potential_successors.append(potential_game_state)

        return potential_successors
    
    #same as generateSuccessors but an action is given for the ai snake to take
    #action in the form "up", "down", "left", "right"
    def generateSuccessorsAction(self, action):
        # Check that successors exist
        if self.isWin() or self.isLose() or self.isDraw(): raise Exception('Can\'t generate a successor of a terminal state.')
        # *hard* copy current state
        state = self.deep_copy()
        # make snake class instances to hold both snakes
        snake_me = Me_Snake(state)
        snake_opp = Opp_Snake(state)
        # List storing all possible successor states
        potential_successors = []

        # Have agents make one random move
        potential_moves = self.get_legal_actions(1)
        # Iterate through, generating a next state for each potential move for each agent
        # (Any combination of either agent's move)
        for move_opp in potential_moves:
            # Have a fresh copy of our snkae and game state
            potential_snake_me_state = snake_me.deep_copy()
            potential_snake_opp_state = snake_opp.deep_copy()
            potential_game_state = state.deep_copy()
            # Update a hard copied snake, update a hard copied gamestate in that snake
            potential_snake_me_state.make_move(action)
            potential_snake_opp_state.make_move(move_opp)
            potential_game_state.me_dx = potential_snake_me_state.dx
            potential_game_state.me_dy = potential_snake_me_state.dy
            potential_game_state.opp_dx = potential_snake_opp_state.dx
            potential_game_state.opp_dy = potential_snake_opp_state.dy
            # Okay, so above we edited the snake's directions, now we have
            # to move the snakes forward one time step
            potential_game_state.step()
            # Check if apple was eaten, if it was replace it using the game logic found in
            # ediblestwoplayer in our state variable above so next time it's
            # copied, it's copied with the new apple, and add one to the length of
            # the snake that ate it
            self.did_eat()
            # Check if the game ended. If so, return a state that displays that.
            if self.isWin() or self.isDraw() or self.isLose():
                self.gameOver = True
            # add the generated potential state to potential_successors
            potential_successors.append(potential_game_state)

        return potential_successors
    
    #gets a single random successor game state from an action
    def generateRandomSuccessor(self, action):
        # Check that successors exist
        if self.isWin() or self.isLose() or self.isDraw(): raise Exception(f'Can\'t generate a successor of a terminal state. {self.gameOver}')
        # *hard* copy current state
        state = self.deep_copy()
        # make snake class instances to hold both snakes
        snake_me = Me_Snake(state)
        snake_opp = Opp_Snake(state)
        # List storing all possible successor states
        potential_successors = []

        # Have agents make one random move
        player_potential_moves = self.get_legal_actions(1)
        move_opp = random.choice(player_potential_moves)
        # Iterate through, generating a next state for each potential move for each agent
        # (Any combination of either agent's move)
        # Have a fresh copy of our snkae and game state
        potential_snake_me_state = snake_me.deep_copy()
        potential_snake_opp_state = snake_opp.deep_copy()
        potential_game_state = state.deep_copy()
        # Update a hard copied snake, update a hard copied gamestate in that snake
        potential_snake_me_state.make_move(action)
        potential_snake_opp_state.make_move(move_opp)
        potential_game_state.me_dx = potential_snake_me_state.dx
        potential_game_state.me_dy = potential_snake_me_state.dy
        potential_game_state.opp_dx = potential_snake_opp_state.dx
        potential_game_state.opp_dy = potential_snake_opp_state.dy
        # Okay, so above we edited the snake's directions, now we have
        # to move the snakes forward one time step
        potential_game_state.step()
        # Check if apple was eaten, if it was replace it using the game logic found in
        # ediblestwoplayer in our state variable above so next time it's
        # copied, it's copied with the new apple, and add one to the length of
        # the snake that ate it
        self.did_eat()
        # Check if the game ended. If so, return a state that displays that.
        if self.isWin() or self.isDraw() or self.isLose():
            self.gameOver = True
        return potential_game_state

    # Increments the snakes based on the direciton they are moving by one time step (or update)
    def step(self):
        '''Update using logic similar to what the pre-existing update function already does
        which is copied below. Just have to edit it for use with a gamestate?
        Also need to pass in the snakes?'''
        #agent 1 is opponent
        #agent 2 is ai
        #got rid of the color stuff cause this should just be for simulation not display
        #got rid of is_collide function for same reason cause it was only to stop music and stuff

        #update position of the first tail's elements
        for i in range(len(self.opp_tail) - 1, 0, -1):
            self.opp_tail[i].x = self.opp_tail[i - 1].x
            self.opp_tail[i].y = self.opp_tail[i - 1].y
        self.opp_tail[0].x, self.opp_tail[0].y = (self.opp_head.x, self.opp_head.y)
        # The following two lines update the x and y position of the first snake's head
        self.opp_head.x += self.opp_dx
        self.opp_head.y += self.opp_dy
        # Checks if any of the game win / game over states and have been met and if so then the function ceases to
        # execute
        if self.isLose() or self.isWin() or self.isDraw():
            return
        # update position of the second tail's elements
        for i in range(len(self.me_tail) - 1, 0, -1):
            self.me_tail[i].x = self.me_tail[i - 1].x
            self.me_tail[i].y = self.me_tail[i - 1].y
        self.me_tail[0].x, self.me_tail[0].y = (self.me_head.x, self.me_head.y)
        # The following two lines update the x and y position of the first snake's head
        self.me_head.x += self.me_dx
        self.me_head.y += self.me_dy

    # This function decides whether or not an apple has been eaten by the snake and if so it then adds a new segment to
    # the snake and spawns in a new apple
    def did_eat(self):
        # Boolean value representing whether or not a space is empty. This matters as you don't want the apple spawning
        # on the same spot as part of the snake's body
        spaceEmpty = True
        # This conditional statement checks whether or not the apple and head of the first snake occupy the same spot
        if self.opp_head.x == self.apple.x and self.opp_head.y == self.apple.y:
            # The integer value of what will be the previous X value
            prevX = self.apple.x
            # The integer value of what will be the previous Y value
            prevY = self.apple.y
            # The integer value of what will be the new current X value. It is randomly generated
            currX = self.myround(random.randint(0, int(self.w / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # This loop checks if the previous X value and the newly generated X value are the same, if so it will
            # generate a new one until they no longer match. This stops the apple from spawning in place
            while prevX == currX:
                currX = self.myround(random.randint(0, int(self.w / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # The integer value of what will be the new current Y value. It is randomly generated
            currY = self.myround(random.randint(0, int(self.h / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # This loop checks if the previous Y value and the newly generated Y value are the same, if so it will
            # generate a new one until they no longer match. This stops the apple from spawning in place
            while prevY == currY:
                currY = self.myround(random.randint(0, int(self.h / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # The next 11 lines essentially do what the previous lines have except it checks each segements of the tail
            # so that the apple doesn't spawn in one of their spots
            for i in self.opp_tail:
                if currX == i.x and currY == i.y:
                    spaceEmpty = False
                    while not spaceEmpty and prevX != currX and prevY != currY:
                        currX = self.myround(random.randint(0, int(self.w / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
                        currY = self.myround(random.randint(0, int(self.h / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
                        for j in self.opp_tail:
                            if currX == j.x and currY == j.y:
                                spaceEmpty = False
                                break
                            spaceEmpty = True

            # Once all has been said and done the apple's x and y values are changed to currX and currY
            self.apple.x = currX
            self.apple.y = currY

            # A new segment is added to the end of the first player's snake
            self.opp_tail.append(Entity(self.opp_tail[len(self.tail_1) - 1].x * self.director.scale, self.opp_tail[len(self.opp_tail) - 1 * self.director.scale].y, 9 * self.director.scale, 9 * self.director.scale, self.director.p1color))

        # This conditional statement checks whether or not the apple and  head of the second snake occupy the same spot
        if self.me_head.x == self.apple.x and self.me_head.y == self.apple.y:
            # The integer value of what will be the previous X value
            prevX = self.apple.x
            # The integer value of what will be the previous Y value
            prevY = self.apple.y
            # The integer value of what will be the new current X value. It is randomly generated
            currX = self.myround(random.randint(0, int(self.w / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # This loop checks if the previous X value and the newly generated X value are the same, if so it will
            # generate a new one until they no longer match. This stops the apple from spawning in place
            while prevX == currX:
                currX = self.myround(random.randint(0, int(self.w / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # The integer value of what will be the new current Y value. It is randomly generated
            currY = self.myround(random.randint(0, int(self.h / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # This loop checks if the previous Y value and the newly generated Y value are the same, if so it will
            # generate a new one until they no longer match. This stops the apple from spawning in place
            while prevY == currY:
                currY = self.myround(random.randint(0, int(self.h / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
            # The next 11 lines essentially do what the previous lines have except it checks each segements of the tail
            # so that the apple doesn't spawn in one of their spots
            for i in self.me_tail:
                if currX == i.x and currY == i.y:
                    spaceEmpty = False
                    while not spaceEmpty and prevX != currX and prevY != currY:
                        currX = self.myround(random.randint(0, int(self.w / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
                        currY = self.myround(random.randint(0, int(self.h / 10 - 10 * self.director.scale)), 10 * self.director.scale) * 10 + 1 * self.director.scale
                        for j in self.tail_2:
                            if currX == j.x and currY == j.y:
                                spaceEmpty = False
                                break
                            spaceEmpty = True

            # Once all has been said and done the apple's x and y values are changed to currX and currY
            self.apple.x = currX
            self.apple.y = currY

            # A new segment is added to the end of the first player's snake
            self.me_tail.append(Entity(self.me_tail[len(self.me_tail) - 1].x * self.director.scale, self.me_tail[len(self.me_tail) - 1 * self.director.scale].y, 9 * self.director.scale, 9 * self.director.scale, self.director.p2color))

    # Function for rounding numbers to multiples of a specified number, that number being the "base" value
    def myround(self, x, base=5):
        return int(base * round(float(x) / base))
