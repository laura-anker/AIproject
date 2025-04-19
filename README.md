# Report
State Space:
Our game state contains the following:
- heads of both snakes (front coordinate of the snakes)
- tails of both snakes (list of coordinates of tails)
- the x and y directions of both snakes
- the apple coordinate
- the walls
- Other things are included for styling including the width, height, scale, screen, and scene

The snakes can each take one of the actions {up, down, left, right} at each time step, but in reality there are only 3 options because the snake cannot move backwards into itself

The observations used to inform the next move include the position of the apple, the position of the other snake (including head and tail), the direction they are moving, the position of yourself (your own tail) and the location of the walls. In other words, the observation of each snake includes the full game state, but they cannot observe the next move that their opponent is going to make. 

To transition from state to state given current observations and available actions goes like this:
- if the snakes' heads collide, there is a draw
- if one snake run's into any snake's tail or a wall, then it dies and the other wins
- if a snake gets to the apple, the snake's tail grows one longer at the end and the apple is regenerated at another open square on the board
- at every step, the snake moves forward in it's a direction, with the head moving to the coordinate in the correct direction, and each tail cooridinate moving behind it. The player snake moves in it's curren't direction unless changed by a keyboard event. The AI snake will run the monte carlo tree search at every step to determine the action it will take based on observation of the game state. 
