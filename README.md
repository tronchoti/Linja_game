# Linja
Linja boardgame programmed in Python. You can play either with another friend or against the AI.


## HOW TO PLAY
The board is divided in 8 rows, where in each of them you can fit a maximum of 6 pieces, no matter what colour they are.

The initial distribution of the board is as the following:
<img src="./images/tablero.jpg" alt="tablero" width="300" height="auto" >

Like in every adversary game, turns will be alternated between both players. In each turn, each player will have at least 1 move.

## RULES
For this game you will find many different rules sets.
## :triangular_ruler: ALGORITHMS USED
For the development of the AI used in this game, two algorithms were used. **MiniMax** and **Alpha Beta**. Both will be explained:
### :small_red_triangle::small_red_triangle_down: MINIMAX
Minimax is a very common algorithm used for adversary games where both players play against each other. It consists of two parts.
The first one is the *maximize* part, which consist in selecting the tree branch that gives the best score to the AI. On the other hand, the *minimize* part consist in choosing the branch that gives the enemy player the best score. Both selections are done based in an heuristic function.

#### :1234: HEURISTIC FUNCTION
In order to be able to evaluate if a move is good or not for one of the players, we need to evaluate the board state. In the case of Linja, we 

### :scissors: ALPHA BETA PRUNNING
