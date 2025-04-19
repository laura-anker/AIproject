'''opponent snake is player/player 1, me is the ai/player 2'''
from Entity import Entity
from OppSnakeUtil import Opp_Snake
from MeSnakeUtil import Me_Snake

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
        return copied_game_state

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
        potential_moves = ["up", "down", "left", "right"]
        # Iterate through, generating a next state for each potential move for each agent
        # (Any combination of either agent's move)
        for move_me in potential_moves:
            for move_opp in potential_moves:
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

                # Check if apple was eaten, if it was replace it using the game logic found in
                # ediblestwoplayer in our state variable above so next time it's
                # copied, it's copied with the new apple, and add one to the length of
                # the snake that ate it
                
                # Check if the game ended. If so, return a state that displays that.

                # add the generated potential state to potential_successors
                potential_successors.append(potential_game_state)

        return potential_successors

    # Increments the snakes based on the direciton they are moving by one time step (or update)
    def step(self):
        # Update using logic similar to what the pre-existing update function already does
        # which is copied below. Just have to edit it for use with a gamestate?
        # Also need to pass in the snakes?

        # update position of the first tail's elements
        # for i in range(len(self.tail_1) - 1, 0, -1):
        #     self.tail_1[i].x = self.tail_1[i - 1].x
        #     self.tail_1[i].y = self.tail_1[i - 1].y
        # self.tail_1[0].x, self.tail_1[0].y = (self.head_1.x, self.head_1.y)
        # # The following two lines update the x and y position of the first snake's head
        # self.head_1.x += self.dx1
        # self.head_1.y += self.dy1
        # # The following three lines ensure that the head and tail of the snake are the proper color as the color
        # # can change if the player picks a new color on the configuration screen
        # self.head_1.color = self.director.p1color
        # for i in self.tail_1:
        #     i.color = self.director.p1color
        # # Calling of the is_collide function
        # self.is_collide()
        # # Checks if any of the game win / game over states and have been met and if so then the function ceases to
        # # execute
        # if self.plyrdraw or self.plyronewins or self.plyrtwowins:
        #     return
        # # update position of the second tail's elements
        # for i in range(len(self.tail_2) - 1, 0, -1):
        #     self.tail_2[i].x = self.tail_2[i - 1].x
        #     self.tail_2[i].y = self.tail_2[i - 1].y
        # self.tail_2[0].x, self.tail_2[0].y = (self.head_2.x, self.head_2.y)
        # # The following two lines update the x and y position of the first snake's head
        # self.head_2.x += self.dx2
        # self.head_2.y += self.dy2
        # # The following three lines ensure that the head and tail of the snake are the proper color as the color
        # # can change if the player picks a new color on the configuration screen
        # self.head_2.color = self.director.p2color
        # for i in self.tail_2:
        #     i.color = self.director.p2color
        # # Calling of the is_collide function
        # self.is_collide()
