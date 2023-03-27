# Tic-tac-toe

## Starting up servers
To start servers run:
- update `/src/config.py` with your node addresses
- `cd src`
- `python main.py`
- input node id from `[0,1,2]`

## Starting the game
To start a new game run `start-game` command. The election will be performed using Ring agorithm to elect a game master, the game master will perform clock sync with the other nodes using Berkley algorithm, then the players will be assigned and notified.

A node can not start a new game when the previous game is still in progress.

## Taking a turn
To take a turn player can run `set-symbol [position]` command. If this is successful - both players will be notified and sent the current board state for visibility.

Only player nodes can place a symbol. A player can only place a symbol into an unoccupied space on the board. A player can not go twice in a row. If the game master detects a time desync with the player during them making their turn - it will not allow to place a symbol.

If after the turn one of the players wins - the game ends and the players are notified, resetting each node's state.

## Adjusting time
The node can adjust time using `set-node-time [server-id] [hh:mm:ss]` command.

Game master can adjust time on any node, but a player can only adjust their node.

## Listing board
To see the board run `list-board` command. It outputs current board state as well as the turn history.

## Timeouts
By default if no player takes a turn for 1 minute the game master will automatically end the game and if a player doesn't hear from the server in 3 minutes it ends the game for itself and reset its state. These times can be adjusted on any node with `set-time-out [game-master | players] [min]` command.
