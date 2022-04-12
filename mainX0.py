
import copy
import time

MAX_DEPTH = 9


class Game:
    NR_LINES = 3
    NR_COL = 3
    SYM_PLAYERS = ['X', 0]
    JMIN = '0'  #None
    JMAX = 'X'  #None
    EMPTY = '#'

    def __init__(self, board=None):
        self.matr = board or [Game.EMPTY] * (Game.NR_LINES * Game.NR_COL)

    @classmethod
    def opponent(cls, player):
        return cls.JMAX if player == cls.JMIN else cls.JMIN

    def same_elem(self, list):
        if (len(set(list)) == 1 and list[0] != Game.EMPTY):
            return list[0]
        return False

    def final(self):
        """
        012
        345
        678
        """
        result = (self.same_elem(self.matr[0:3]) or self.same_elem(self.matr[3:6]) or self.same_elem(
            self.matr[6:]) or  # lines
                  self.same_elem(self.matr[0:9:3]) or self.same_elem(self.matr[1:9:3]) or self.same_elem(
                    self.matr[2:9:3]) or  # columns
                  self.same_elem(self.matr[0:9:4]) or self.same_elem(self.matr[2:8:2])  # diag
                  )

        if (result != False):
            return result
        if (Game.EMPTY not in self.matr):
            return "remiza"
        return False

    def moves_game(self, player):  # the symbol of the current player
        all_moves = []  # a list of "games" with all configuration possible
        for i in range(len(self.matr)):
            if self.matr[i] == Game.EMPTY:
                matrix_copy = copy.deepcopy(self.matr)
                matrix_copy[i] = player
                all_moves.append(matrix_copy)
        return all_moves

    def open_line(self, list, player):
        opponent = None
        if (player == Game.JMAX):
            opponent = Game.JMIN
        else:
            opponent = Game.JMAX
        if (opponent not in list):
            return 1
        return 0

    def chances(self, player):  # on how many directions the current player can extend
        result = self.open_line(self.matr[0:3], player) + self.open_line(self.matr[3:6], player) + self.open_line(
            self.matr[6:], player) + self.open_line(self.matr[0:9:3], player) + self.open_line(self.matr[1:9:3],
                                                                                               player) + self.open_line(
            self.matr[2:9:3], player) + self.open_line(self.matr[0:9:4], player) + self.open_line(self.matr[2:8:4],
                                                                                                  player)

    def estimate_final(self, depth):
        result = self.final()
        if (result):  # it is final configuration
            if (result == "remiza"):
                return 0
            if (result == Game.JMAX):
                return 999 + depth
            return -999 - depth

        # it's not final configuration
        return self.chances(Game.JMAX) - self.chances(Game.JMIN)

################todo print

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COL)]) + "\n"
        sir += "-" * (self.NR_COL + 1) * 2 + "\n"
        for i in range(self.NR_COL):  # itereaza prin linii
            sir += str(i) + " |" + " ".join(
                [str(x) for x in self.matr[self.NR_COL * i: self.NR_COL * (i + 1)]]) + "\n"
        # [0,1,2,3,4,5,6,7,8]
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()

class State:
    # it will not be modified during the algorithm
    MAX_DEPTH = 9 #how much we can extend the searching tree'

    #IT WILL MODIFY FROM A STATE OF A GAME TO ANOTHER, DEPENDING ON A VALID MOOVE
    def __init__(self, board, current_player, depth, parent = None, score = None):
        self.board = board  #an object "Game --> board.matr
        self.current_player = current_player    #the symb of the current player
        self.depth = depth  #the depth of the tree, it will be decreased from parent->child
        self.score = score   #the score of the state if it's final(a leaf of the tree) or the cost of the best child
        self.possible_moves = [] #list with "States" --> all possible moves from current
        self.best_move = None #that will be the chosen one

    def moves_from_state(self): #return a list of states
        list_moves = self.board.moves_game(self.current_player)
        opponent_player = Game.opponent(self.current_player)
        resulted_states = []
        for move in list_moves:
            new_state = State(move, opponent_player, self.depth - 1,  self)
            resulted_states.append(new_state)
        return resulted_states

    ################todo print
    def __str__(self):
        sir = str(self.board) + "(Juc curent:" + self.current_player + ")\n"
        return sir

    def __repr__(self):
        return self.current_player + str(self.board)


#param: a state and returns  the state modified --> scor, possible_moves &best_move
#returns the state modified
def min_max(state):
    #if we are in A FINAL STATE:
    #-we have expanded at maximum or we are in a final state
    if state.depth == 0: #or state.board.final():
        state.score = state.board.estimate_score(state.depth)
        return state

    #otherwise, calculate all the possible moves from current state
    state.possible_moves = state.moves_from_state()

    #apply the min_max for all it's childs --> calculate the trees
    scores_moves = [min_max(move) for move in state.possible_moves]

    if state.current_player == Game.JMAX:
        #we will choose the highest score
        state.best_move = max(scores_moves, key = lambda x:x.score)
    else:
        #we will choose the minimum
        state.best_move = min(scores_moves, key = lambda x:x.score)

    #update the father's score with the child's
    state.score = state.best_move.score

    return state

####todo print

def print_if_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()  # metoda final() returneaza "remiza" sau castigatorul ("x" sau "0") sau False daca nu e stare finala
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)
        return True
    return False

def main():
    #init algo
    valid_response = False
    while not valid_response:
        type_algo = input("The algorithm to use:\n 1)Minmax\n 2)Alpha-beta\n")
        if type_algo in ['1', '2']:
            valid_response = True
        else:
            print("Invalid input")

    #init players
    valid_response = False
    while not valid_response:
        Game.JMIN = input("Play with x or 0\n").upper()
        if(Game.JMIN in ['X', '0']):
            valid_response = True
        else:
            print("Invalid input")
    Game.JMAX = '0' if Game.JMIN == 'X' else 'X'

    #init board
    current_board = Game();
    print("Table:")
    print(str(current_board))
    current_state = State(current_board, 'X', MAX_DEPTH)#always starts X


    while True:
        # if current_state.current_player == Game.JMIN: #the user turn
        #     valid_response = False
        #     while not valid_response:
        #         try:
        #             line = int(input("Line:"))
        #             col = int(input("Column:"))
        #             if(line in range(Game.NR_LINES) and col in range(Game.NR_COL)):
        #                 if(current_state.board[line * Game.NR_COL + col] == Game.EMPTY):
        #                     valid_response = True
        #                 else:
        #                     print("There is already a symbol here")
        #             else:
        #                 print("Invalid input for line or column, please choose a number from 0 to 2")
        #         except ValueError:
        #             print("Plese input an integer number from 0 to 2")
        #
        #     #make the moove
        #     #current_state.board.matr[line * Game.NR_COL + col] = Game.JMIN
        #     current_state.board.matr[line * current_state.board.NR_COL + col] = current_state.board.JMIN
        #     print("The table after the move\n")
        #     print(str(current_state))
        #     if (print_if_final(current_state)):
        #         break
        #     #change the player
        #     current_state.current_player = Game.opponent(current_state.current_player)
        #
        # else: #JMAX --> the computer
            print("Now the computer")
            t_before = int(round(time.time()) * 1000)

            if type_algo == '1':
                updated_state = min_max(current_state) #it's the current board where we update the next move
            else:       ##toDO alpha beta
                break

            current_state.board = updated_state.best_move.board #change just the boards and the player
            current_state.current_player = Game.opponent(current_state.current_player)
            t_after = int(round(time.time()) * 1000)

            print("The computer has thought" + str(t_after - t_before) + "milliseconds")
            if(print_if_final(current_state)):
                break








# game = Game(['#', '#', '#', '0', '0', '0', '0', '#', '0'])
# #print(game.estimate_final(9))
#
# state = State(game, 'X', 9)
# print(state)
# print(state.moves_from_state())

if __name__ == "__main__":
    main()
