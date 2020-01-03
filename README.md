# Board Game

Simple game with Intelligent Agents 

GAME RULES
**********************************************************************************************
1. At the beginning of the game, four seeds are placed in each house.

2. Each player controls the six houses and their seeds on the player's side of the board.
   The player's score is the number of seeds in the store to their right.

3. Players take turns sowing their seeds. On a turn, the player removes all seeds from one
   of the houses under their control. Moving counter-clockwise, the player drops one seed in
   each house in turn, including the player's own store but not their opponent's.

4. If the last sown seed lands in an empty house owned by the player, and the opposite house
   contains seeds, both the last seed and the opposite seeds are captured and placed into
   the player's store.

5. If the last sown seed lands in the player's store, the player gets an additional move.
   There is no limit on the number of moves a player can make in their turn.

6. When one player no longer has any seeds in any of their houses, the game ends.
   The other player moves all remaining seeds to their store, and the player with the
   most seeds in their store wins.
**********************************************************************************************

HOW TO RUN THE PROGRAM
**********************************************************************************************
1. All source codes are included in /src directory;
2. Use any IDE or command prompt to execute file [  main.py  ];
3. Exmaple execution in command prompt: [ Python main.py ]
4. Once executed, the menu will be displayed as -


**********************************************************
   Welcome to the Mancala Game!
   Please Choose a Type for Player 1 and Player 2:
   Menu: 2 - human
         3 - random
         4 - minimax
         5 - minimax with alpha_beta pruning
   Please enter the corresponding number only.

   Player 1:
   Player 2:

**********************************************************

1. Enter types for player 1 and player 2:
   e.g. 2 [ENTER] 
        4 [ENTER] 
   for Human vs. Minimax
2. Game starts once receiving player types in the correct format;
3. When game ends, user will be prompted to start a new game;
4. If user wishes to modify maximum depth for Minimax or Alpha-Beta, do the following - 
   - Find command [ Game(player_one, name_one, player_two, name_two, 6, 6).play() ] 
     in line [405];
   - The first 6 in the line specifies max depth for Minimax;
   - The first 6 in the line specifies max depth for Alpha-Beta;
5. WARNING: depth beyond 7 for Minimax and 9 for Alpha-Beta are not recommended for 
   optimal gaming experience;
