# Report

Problem:
We decided to create a 2-player snake game where one of the snakes is controlled by a player and the other snake is an AI. 

Similar Problems and Solutions:
- https://www.greenfoot.org/scenarios/26534 This solution uses A* search to make a single snake go to an apple. It does not account for the possibility of a second snake and it can also run into itself or a wall if there is no current path to the apple, therefore failing when the length gets long.
- https://eric.guldbrand.io/two-player-snake/ This solution uses the Monte Carlo Tree search algorithm for two player Snake. It was created by Algot Johansson and Eric Guldbrand and implemented in Kotlin. It runs into an issue where the snakes tend to draw by trying to enter the same square at the same time. We could improve upon this by adding an extra ruling to indicate the possibility of a draw if the two snakes’ heads collide. 
- https://github.com/sds-dubois/snake.ai This project was created by Sebastien Dubois, Sebastien Levy, and Felix Crevier. This game is slightly more complex as it is inspired by slither.io and features multiple snakes which turn into food when they die. They experimented with using linear functions, neural nets, and minimax and found their neural nets approach to be most effective, though the minimax beat the linear model at certain depths.

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


Our Solution:

We started by developing the game state in UtilTwoSnake.py. The game state included information about the positions of the two snakes, the directions of the two snakes, the apple, and the game board. Some key methods included 
- get_legal_actions method, which returns a list of potential actions a snake can take given it's current direction,
- generateSuccessorsAction method, which generates a list of potential successor game states given a game state and an action for the snake to take,
- generateRandomSuccessor, which generates a single random successor state from a game state and an action,
- get_winner, which returns the winning agent or a draw if the game is over,
- get_apple, which returns how many times a given agent has eaten an apple

Next, we implemented the Monte Carlo Tree Search in MCTS.py. The key methods in this are:
- select_ucb1, selects a node to expand using the UCB1 formula,
- expand, expands the node selected by using the generateRandomSuccessor method and adding a new node as a child
- simulate, uses generateRandomSuccessor repeatedly until a terminal state is found from the get_winner method. Returns a score based on whether a win/loss/draw was reached and how many times an apple was simulated being eaten using the get_apple method
- backpropogate, travels up the tree from the simulated node, adding to the score and visit count
- run, runs the previous methods for a given time, then calculates the best action to take from the scores of the root's child nodes

Finally, we ran the Monte Carlo Tree Search on the current game state in the EdiblesTwoPlayer.py on_update method and implement the given move. 

Outcome:
Overall, we believe that we successfully implemented Monte Carlo Tree Search, however, there were some challenges with the problem that lead to the game play being sub-par to what we initially envisioned. If you run the two-player game, you will find that the majority of the time the snake randomly wiggles around the board, usually avoiding the walls and the player snake. If the mcts snake gets close to the apple, it will usually try to eat it, but doesn't if the apple is far away. We believe the reason for this is that the tree search doesn't simulate far enough down to see itself eating the apple. Another issue is that sometimes the snake will kill itself by running into a wall or itself. Upon further examination, this was the result of poor chance. If the MCTS was able to run longer than better choices would likely be made, however this would result in a very slow, unplayable game. Some of the things we tried to improve game play were:
- using a separate thread to run the MCTS. This had the benefit of being able to play the game faster and allowing the tree to run longer and simulate more, but is caused some critical unpredictable inconsistancies in performance, so we decided to stop using multithreading and instead have the tree run for less time but with consistancy.
- Adding the get_apple method to give a boost to actions that would result in the snake eating the apple. The long term benefits of having a longer snake from eating apples was simply too far down the tree for the MCTS to see, so by adding the extra boost to get_apple, this motivated the snake to eat the apple at least a little
- Adding the rebase_tree method in MCTS.py. This method checks to see if the current game state has already been generated in the tree, and if so, makes that node the new state, if not resets the tree entirely. This was intended to let the tree be longer by re-using already generated nodes at next steps. However, we didn't actually see the tree being rebased because it didn't find the current state in the pre-generated states. This is likely because there are simply so many possible successor states from a given game state that the odds of the the actual next state being generated as a child of the root is very low.

Despite these challenges, we saw the MCTS output good choices given the available resources. Below is an example of the result of a typical tree search. The first 4 numbers are the number of total simulated wins, losses, draws, and times the mcts snake ate the apple. Below, are the children of the root with their actions, scores, and number of visits. The final action was chosen by dividing total score by number of visits for a given action. In this example, eating an apple was valued at 500, explaining the high score. The snake chose left, which was valued highly for it's probability of winning and eating the apple. 
![image](https://github.com/user-attachments/assets/6bd058c5-3bab-4d6a-8137-c4410057925f)
