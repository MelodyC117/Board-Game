"""
AUTHOR: Melody Chen @ UR CSC 442 (31620871 | mchen73@ur.rochester.edu)
"""

import random
import sys
from copy import deepcopy
import time

class Board:
    "initilize board, index list and position maps for both players"
    def __init__(self):
        self.board = [0, 4, 4, 4, 4, 4, 4,
                      0, 4, 4, 4, 4, 4, 4]

        self.player1_index = [1, 2, 3, 4, 5, 6]
        self.player2_index = [8, 9, 10, 11, 12, 13]

        self.map1 = {1: 13, 2: 12, 3: 11, 4: 10, 5: 9, 6: 8}
        self.map2 = {13: 1, 12: 2, 11: 3, 10: 4, 9: 5, 8: 6}

        self.display()

    "display board"
    def display(self):
        print("_________________________________________________________________________")
        print("************************** WELCOME TO MANCALA ***************************")
        print()
        print(" POSITION#        #13   #12   #11     #10   #09   #08")
        print("            ---------------------------------------------")
        print("                |  %s  |  %s  |  %s  |||  %s  |  %s  |  %s  |" % (self.board[13], \
                                                                                 self.board[12], \
                                                                                 self.board[11], \
                                                                                 self.board[10], \
                                                                                 self.board[9], \
                                                                                 self.board[8]))
        print("     ---------------------------------------------------------------")
        print("      #01 |  %s  |   <- Player One  vs.  Player Two ->   |  %s  | #07" % (self.board[0], \
                                                                                         self.board[7]))
        print("     ---------------------------------------------------------------")
        print("                |  %s  |  %s  |  %s  |||  %s  |  %s  |  %s  |" % (self.board[1], \
                                                                                 self.board[2], \
                                                                                 self.board[3], \
                                                                                 self.board[4], \
                                                                                 self.board[5], \
                                                                                 self.board[6]))
        print("            ---------------------------------------------")
        print("                  #01   #02   #03     #04   #05   #06          #POSITION")
        print("_________________________________________________________________________")

    "find player's row and map each pit to the opponent's direct opposite pit"
    def find_index(self, player):
        if player == 1:
            index, position = self.player1_index, self.map1
        else:
            index, position = self.player2_index, self.map2

        return index, position

    "find the current player's opponent number"
    def find_opponent(self, player):
        if player == 1:
            return 0
        else:
            return 1

    "check whether a given move is legal"
    def is_legal(self, player, pit):
        index, position = self.find_index(player)

        if pit not in index or self.board[pit] == 0:
            return False
        else:
            return True

    "return a list of legal moves represented by nonzero pit numbers"
    "pit numbers must be in current player's row"
    def legal_move(self, player):
        index, position = self.find_index(player)

        moves = []
        for i in index:
            if self.board[i] != 0:
                moves.append(i)

        # print("Available Moves: ", moves)
        return moves

    "make the given move, accumulate points according to the rules"
    "decide whether to grant an extra - if last marble ends in player's own Mancala"
    def make_move(self, player, pit):
        index, position = self.find_index(player)

        if not pit or not self.board[pit]:
            return False

        stones = self.board[pit]
        # print("Move Chosen:", pit)
        # print("Current Stones to be Distributed:", stones)
        self.board[pit] = 0
        while stones:
            stones -= 1
            pit = (pit + 1) % 14
            if pit != (index[-1] + 1) % 14:
                self.board[pit] += 1
            else:
                pit += 1
                self.board[pit] += 1

        if self.board[pit] == 1 and pit in index:
            # print("Landed in current player's own pit?", self.board[pit] == 1 and pit in index)
            opponent_pos = position[pit]
            # print("Corresponding opponent position:", opponent_pos)
            # print("Stones to be collected:", self.board[opponent_pos])

            self.board[index[0]-1] += self.board[opponent_pos]
            self.board[index[0]-1]  += self.board[pit]
            # print("Mancala collected", self.board[opponent_pos], "stones")
            self.board[opponent_pos] = 0
            self.board[pit] = 0

        if pit == index[0]-1:
            # print("Landed in player's own Mancala? ", pit == index[0]-1)
            return True

        return False

    "calculate both player's total points including Mancala + all remains on the board"
    def scoreboard(self, player):
        player_count, opponent_count = 0, 0
        index, position = self.find_index(player)
        opponent = self.find_opponent(player)
        opp_index, opp_position = self.find_index(opponent)

        for i, j in zip(index, opp_index):
            player_count += self.board[i]
            opponent_count += self.board[j]

        player_count += self.board[index[0]-1]
        opponent_count += self.board[opp_index[0]-1]

        return player_count, opponent_count, player_count-opponent_count

    "check whether game should end - when one side is cleared out"
    def terminated(self):
        if sum(self.board[1:7]) == 0 or sum(self.board[8:14]) == 0:
            return True
        return False

class Player:
    "coordinate min and max functions"
    def play_minimax(self, turn, board, depth):
        counter = 1
        start = time.time()
        best_value, best_move = float('-inf'), -1
        for i in board.legal_move(turn):
            if depth == 0 or board.terminated():
                return best_move, 0, counter
            practice_board = deepcopy(board)
            practice_board.make_move(turn, i)
            opponent = practice_board.find_opponent(turn)
            current, count = self.min_move(opponent, practice_board, depth-1)
            counter += count
            if current > best_value:
                best_value = current
                best_move = i
        end = time.time()
        elapsed = end - start
        return best_move, elapsed, counter

    "call min function to iteratively determine the max utility"
    def max_move(self, turn, board, depth):
        counter = 1
        if depth == 0 or board.terminated():
            return self.utility(board, turn), counter
        best_value = float('-inf')
        for i in board.legal_move(turn):
            practice_board = deepcopy(board)
            practice_board.make_move(turn, i)
            opponent = practice_board.find_opponent(turn)
            current, count = self.min_move(opponent, practice_board, depth-1)
            counter += count
            best_value = max(best_value, current)
        return best_value, counter

    "call max function to iteratively determine the min utility"
    def min_move(self, turn, board, depth):
        counter = 1
        if depth == 0 or board.terminated():
            return self.utility(board, turn), counter
        best_value = float('inf')
        for i in board.legal_move(turn):
            practice_board = deepcopy(board)
            practice_board.make_move(turn, i)
            opponent = practice_board.find_opponent(turn)
            current, count = self.max_move(opponent, practice_board, depth-1)
            counter += count
            best_value = min(best_value, current)
        return best_value, counter

    "coordinate AB min and max functions"
    def play_alphabeta(self, turn, board, depth, alpha=float('-inf'), beta=float("inf")):
        counter = 1
        start = time.time()
        best_value, best_move = float('-inf'), -1
        for i in board.legal_move(turn):
            if depth == 0 or board.terminated():
                return best_move, 0, counter
            practice_board = deepcopy(board)
            practice_board.make_move(turn, i)
            opponent = practice_board.find_opponent(turn)
            current, count = self.alphabeta_min_move(opponent, practice_board, depth-1, alpha, beta)
            counter += count
            if current > best_value:
                best_value = current
                best_move = i

        end = time.time()
        elapsed = end - start
        return best_move, elapsed, counter

    "call AB min function to iteratively determine the max utility and maximize ALPHA"
    def alphabeta_max_move(self, turn, board, depth, alpha, beta):
        counter = 1
        if depth == 0 or board.terminated():
            return self.utility(board, turn), counter
        best_value = float('-inf')
        for i in board.legal_move(turn):
            practice_board = deepcopy(board)
            practice_board.make_move(turn, i)
            opponent = practice_board.find_opponent(turn)
            current, count = self.alphabeta_min_move(opponent, practice_board, depth-1, alpha, beta)
            counter += count
            best_value = max(best_value, current)
            if best_value >= beta:
                return best_value, counter
            alpha = max(best_value, alpha)
        return best_value, counter

    "call AB max function to iteratively determine the min utility and minimize BETA"
    def alphabeta_min_move(self, turn, board, depth, alpha, beta):
        counter = 1
        if depth == 0 or board.terminated():
            return self.utility(board, turn), counter
        best_value = float('inf')
        for i in board.legal_move(turn):
            practice_board = deepcopy(board)
            practice_board.make_move(turn, i)
            opponent = practice_board.find_opponent(turn)
            current, count = self.alphabeta_max_move(opponent, practice_board, depth-1, alpha, beta)
            counter += count
            best_value = min(best_value, current)
            if best_value <= alpha:
                return best_value, counter
            beta = min(best_value, beta)
        return best_value, counter

    "use net points between the two players as utility function"
    def utility(self, board, turn):
        if turn == 1:
            return board.scoreboard(1)[2]
        else:
            return -1 * board.scoreboard(1)[2]


class Game:
    "initilize a list of variables to track game statistics"
    def __init__(self, player_one, player1_name, player_two, player2_name, d1=4, d2=8):
        self.player_one = player_one
        self.player_two = player_two
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.timer = {player1_name: [], player2_name: []}
        self.d1 = d1
        self.d2 = d2
        self.depth = {player1_name: self.d1, player2_name: self.d2}
        self.moves = {player1_name: [], player2_name: []}
        self.counter = {player1_name: [], player2_name: []}

    "determine player types and execute appropriate programs for each type"
    def player(self, board, turn):
        player_type = self.player_one if turn == 1 else self.player_two
        name = self.player1_name if turn == 1 else self.player2_name
        extra_round = True
        while extra_round:
            if not board.legal_move(turn):
                return board
            print("It's {}'s turn!".format(name))
            if player_type == 2:
                try:
                    move = int(input('Please make your next move or enter -1 to terminate program: '))
                except ValueError:
                    print("Invalid Input!")
                    continue
                if move == -1:
                    self.new_game()
                    sys.exit()
            elif player_type == 3:
                move = random.choices(board.legal_move(turn))[0]
            elif player_type == 4:
                move, elapsed, counter = Player().play_minimax(turn, board, self.d1)
                self.timer[name].append(round(elapsed,3))
                self.counter[name].append(counter)
            elif player_type == 5:
                move, elapsed, counter = Player().play_alphabeta(turn, board, self.d2)
                self.timer[name].append(round(elapsed,3))
                self.counter[name].append(counter)

            if board.is_legal(turn, move):
                print(name, "made move", move)
                self.moves[name].append(move)
                extra_round = board.make_move(turn, move)
                board.display()
            elif move == -1:
                break
            else:
                print("Illegal Move!")

        return board

    "play the game and print out game statistics when game ends"
    def play(self, start_board=None):
        board = Board()
        if start_board is not None:
            board.board = start_board

        start = time.time()
        while True:
            if board.terminated(): break
            board = self.player(board, 1)
            if board.terminated(): break
            board = self.player(board, 0)

        end = time.time()
        elapsed = end - start

        current, other, difference = board.scoreboard(1)
        print(f"{self.player1_name}'s score:", current)
        print(f"{self.player2_name}'s score:", other)
        if difference > 0:
            print(self.player1_name, "WINS!")
        elif difference < 0:
            print(self.player2_name, "WINS!")
        else:
            print("It's a DRAW.")

        print("---------------------------------------------------------------------")
        print("GAME STATISTICS")
        print("---------------------------------------------------------------------")
        if self.player1_name in ["Minimax", "Minimax_01", "AlphaBeta", "AlphaBeta_01"] and self.player2_name in ["Minimax", "Minimax_02", "AlphaBeta", "AlphaBeta_02"]:
            print("Rounds Duration")
            print(f"  ◙ {self.player1_name}:", self.timer[self.player1_name])
            print("    At Depth:", self.depth[self.player1_name], " | Average Time Spent:", round(sum(self.timer[self.player1_name]) / len(self.timer[self.player1_name]),3))
            print("    Total Branches Expanded:", self.counter[self.player1_name])
            print(f"  ◙ {self.player2_name}:", self.timer[self.player2_name])
            print("    At Depth:", self.depth[self.player2_name], " | Average Time Spent:", round(sum(self.timer[self.player2_name]) / len(self.timer[self.player2_name]),3))
            print("    Total Branches Expanded:", self.counter[self.player2_name])

        print()
        print("Moves Tracked")
        print(f"  ◙ {self.player1_name}:", self.moves[self.player1_name])
        print(f"  ◙ {self.player2_name}:", self.moves[self.player2_name])
        print()
        print("Game Lasted:", round(elapsed,2), "Seconds")

        print()
        self.new_game()

    "ask whether to start a new game"
    def new_game(self):
        again = input("Would you like to play again (Y / N): ")
        if again == "Y" or again == "y":
            interface()


"main function to be called to initilize the menu and get player types"
def interface():
    print("Welcome to the Mancala Game!")
    print("Please Choose a Type for Player 1 and Player 2:")
    print("Menu: 2 - human")
    print("      3 - random")
    print("      4 - minimax")
    print("      5 - minimax with alpha_beta pruning")
    print("Please enter the corresponding number only.")
    input_map = {2: 'Human', 3: 'Random', 4: 'Minimax', 5: 'AlphaBeta'}
    valid = True
    while valid:
        try:
            player_one = int(input("Player 1: "))
            player_two = int(input("Player 2: "))
        except ValueError:
            print("Invalid Input! Must be integer values in [2, 3, 4, 5].")
            continue
        try:
            name_one = input_map[player_one]
            name_two = input_map[player_two]
            valid = False
        except KeyError:
            print("Invalid Input! Must be integer values in [2, 3, 4, 5].")
            continue
    if name_one == name_two:
        name_one += "_01"
        name_two += "_02"

    Game(player_one, name_one, player_two, name_two, 6, 6).play()

if __name__ == "__main__":
    interface()


" BELOW IS A TESTING FUNCTION THAT CONDUCTS SIMULATIONS BETWEEN DIFFERENT PLAYERS"
# def performance(player_one, player_two, laps, d1, d2):
#     input_map = {2: 'Human', 3: 'Random', 4: 'Minimax', 5: 'AlphaBeta'}
#     name_one = input_map[player_one]
#     name_two = input_map[player_two]
#
#     if name_one == name_two:
#         name_one += "_01"
#         name_two += "_02"
#
#     result = []
#     for i in range(laps):
#         result.append(Game(player_one, name_one, player_two, name_two, d1, d2).play())
#
#     return result
#
# result = performance(3, 4, 1000, 4, 9)
# import csv
#
# with open('simulation.csv', mode='w') as file:
#     writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(result)
#
# print(result)
