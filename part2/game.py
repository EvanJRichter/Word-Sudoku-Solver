import time, random

def is_in_bounds(x, y):
    if x >= 0 and x < 8 and y >= 0 and  y < 8:
        return True
    return False

class Player:
    # self.color = None
    # self.strategy = None
    # self.heuristic = None
    # self.pieces = None
    # self.count = None

    def __init__(self, color, strategy, heuristic):
        self.color = color
        self.strategy = strategy
        self.heuristic = heuristic
        self.count = 16
        self.expanded_nodes = 0
        self.total_time = 0
        self.total_moves = 0

class Game:
    # self.board = None
    # self.white = None
    # self.black = None
    # self.turn = None
    # self.opponent = None

    def __init__(self, sw, sb, hw, hb):
        self.board = []
        for i in range (0, 8):
            self.board.append([])
            for j in range (0, 8):
                self.board[i].append("-")

        for i in range (0, 8):
            self.board[i][0] = "w"
            self.board[i][1] = "w"
            self.board[i][6] = "b"
            self.board[i][7] = "b"

        self.white = Player("w", sw, hw)
        self.black = Player("b", sb, hb)
        self.turn = self.white
        self.opponent = self.black

    def play(self):
        print "--------------GAME STARTING--------------"

        print "\nWhite Team"
        print "Strategy:" , self.white.strategy
        print "Heuristic:" , self.white.heuristic

        print "\nBlack Team"
        print "Strategy:" , self.black.strategy
        print "Heuristic:" , self.black.heuristic

        print "\nStarting Team: white"

        count = 0
        while not self.is_game_over() and count < 1000:
            self.move()
            self.alternate_turn()
            count += 1
            # print count
            # self.print_game()
            # time.sleep(2)

        print "\n1. Final board position:"
        self.print_game()

        print "\n2. Total nodes expanded:"
        print "White team:", self.white.expanded_nodes
        print "Black team:", self.black.expanded_nodes

        print "\n3. Average statistics per move:"
        print "White team average number of nodes expanded per move:", self.white.expanded_nodes / self.white.total_moves
        print "Black team average number of nodes expanded per move:", self.black.expanded_nodes / self.black.total_moves
        print "White team average time to make a move:", self.white.total_time / self.white.total_moves
        print "Black team average time to make a move:", self.black.total_time / self.black.total_moves

        print "\n4. Satistics per player:"
        print "White team captured:", 16 - self.black.count
        print "Black team captured:", 16 - self.white.count
        print "Total moves until end:", self.white.total_moves + self.black.total_moves

        return

    def print_game(self):
        board = ""
        for i in range (0, 8):
            for j in range (0, 8):
                board += self.board[i][j] + "|"
            board += "\n"

        board + "\n\n"
        print board

    def move(self):
        start_time = time.time()
        move = self.find_move()
        self.do_move(move[0], move[1])
        runtime = (time.time() - start_time)

        self.turn.total_time += runtime
        self.turn.total_moves += 1

    def find_move(self):
        if self.turn.strategy == "minmax":
            return self.minmax_decision()
        if self.turn.strategy == "alphabeta":
            return self.alpha_beta_search()
        if self.turn.strategy == "random":
            return self.random_decision()

    def alternate_turn(self):
        if self.turn == self.white:
            self.turn = self.black
            self.opponent = self.white
        else:
            self.turn = self.white
            self.opponent = self.black

    def touchdown(self):
        for i in range (0, 8):
            if self.board[i][0] == "b":
                print "\nBlack Team won"
                return True
            if self.board[i][7] == "w":
                print "\nWhite Team won"
                return True
        return False

    def is_game_over(self):
        if self.white.count == 0 or self.black.count == 0 or self.touchdown():
            return True
        return False

    def get_possible_moves(self):
        start = -1
        end = -1
        advance = 0

        if self.turn == self.white:
            start = 0
            end = 7
            advance = 1
        else:
            start = 7
            end = 0
            advance = -1

        possible_moves = []

        for i in range (0, 8):
            for j in range (0, 8):
                if self.board[i][j] == self.turn.color:
                    if is_in_bounds(i, j + advance) and self.board[i][j + advance] == "-":
                        locationA = (i, j)
                        locationB = (i, j + advance)
                        possible_moves.append((locationA, locationB))

                    if is_in_bounds(i + 1, j + advance) and self.board[i + 1][j + advance] != self.turn.color:
                        locationA = (i, j)
                        locationB = (i + 1, j + advance)
                        possible_moves.append((locationA, locationB))

                    if is_in_bounds(i - 1, j+advance) and self.board[i - 1][j + advance] != self.turn.color:
                        locationA = (i, j)
                        locationB = (i - 1, j + advance)
                        possible_moves.append((locationA, locationB))

        return possible_moves

    def do_move(self, locationA, locationB):
        if self.board[locationB[0]][locationB[1]] == "w":
            self.white.count -= 1
        if self.board[locationB[0]][locationB[1]] == "b":
            self.black.count -= 1
        prev = self.board[locationB[0]][locationB[1]]
        self.board[locationB[0]][locationB[1]] = self.board[locationA[0]][locationA[1]]
        self.board[locationA[0]][locationA[1]] = "-"
        return prev

    def undo_move(self, locationA, locationB, prev):
        if prev == "w":
            self.white.count += 1
        if prev == "b":
            self.black.count += 1
        self.board[locationA[0]][locationA[1]] = self.board[locationB[0]][locationB[1]]
        self.board[locationB[0]][locationB[1]] = prev

    def random_decision(self):
        possible_moves = self.get_possible_moves()
        index = random.randint(0, len(possible_moves)-1)
        return possible_moves[index]

    def minmax_decision(self):
        value, move = self.max_value(0)
        return move

    def max_value(self, level):
        if level == 3:
            value = self.evaluate_board()
            return (value, None)

        possible_moves = self.get_possible_moves()
        if not possible_moves:
            value = self.evaluate_board()
            return (value, None)

        max_value = -float("inf")
        max_move = None
        expanded_nodes = 0
        for move in possible_moves:
            self.turn.expanded_nodes += 1
            prev = self.do_move(move[0], move[1])
            value, useless_move = self.min_value(level + 1)
            if value >= max_value :
                max_value = value
                max_move = move
            self.undo_move(move[0], move[1], prev)
        return max_value, max_move

    def min_value(self, level):
        if level == 3:
            value = self.evaluate_board()
            return (value, None)

        possible_moves = self.get_possible_moves()
        if not possible_moves:
            value = self.evaluate_board()
            return (value, None)

        min_value = float("inf")
        min_move = None
        for move in possible_moves:
            self.turn.expanded_nodes += 1
            prev = self.do_move(move[0], move[1])
            value, useless_move = self.max_value(level + 1)
            if value <= min_value :
                min_value = value
                min_move = move
            self.undo_move(move[0], move[1], prev)
        return min_value, min_move

    def alpha_beta_search(self):
        value, move = self.ab_max_value(0, -float("inf"), float("inf") )
        return move

    def ab_max_value(self, level, alpha, beta):
        if level == 5:
            value = self.evaluate_board()
            return (value, None)

        possible_moves = self.get_possible_moves()
        if not possible_moves:
            value = self.evaluate_board()
            return (value, None)

        max_value = -float("inf")
        max_move = None
        for move in possible_moves:
            self.turn.expanded_nodes += 1
            prev = self.do_move(move[0], move[1])
            # v = MAX (v, min_value())
            value, useless_move = self.ab_min_value(level + 1, alpha, beta)
            self.undo_move(move[0], move[1], prev)
            if value >= max_value:
                max_value = value
                max_move = move
            # if v >= b return v
            if value >= beta:
                return value, move
            # a = max(v, a)
            if value >= alpha:
                alpha = value
        return max_value, max_move

    def ab_min_value(self, level, alpha, beta):
        if level == 5:
            value = self.evaluate_board()
            return (value, None)

        possible_moves = self.get_possible_moves()
        if not possible_moves:
            value = self.evaluate_board()
            return (value, None)

        min_value = float("inf")
        min_move = None
        for move in possible_moves:
            self.turn.expanded_nodes += 1
            prev = self.do_move(move[0], move[1])
            # v = MIN (v, max_value())
            value, useless_move = self.ab_max_value(level + 1, alpha, beta)
            self.undo_move(move[0], move[1], prev)
            if value <= min_value :
                min_value = value
                min_move = move
            # if v <= a return v
            if value <= alpha:
                return value, move
            # a = max(v, a)
            if value <= beta:
                beta = value
        return min_value, min_move

    def evaluate_board(self):
        turn = self.get_points(self.turn)
        opponent = self.get_points(self.opponent)

        if self.turn.heuristic == "aggresive":
            return 2 * turn - opponent
        if self.turn.heuristic == "defensive":
            return turn - 2 * opponent


    def get_points(self, team):
        total_holes = 0
        total_winning = 0
        total_almost_winning = 0
        total_attack = 0
        total_defence = 0
        total_moves = 0
        total_dispersion = 0

        holes_weight = -5
        winning_weight = 20
        almost_winning_weight = 10
        attack_weight = 10
        defence_weight = 5
        moves_weight = 10
        dispersion_weight = 5

        start = -1
        end = -1
        advance = 0
        if team == self.white:
            start = 0
            end = 7
            advance = 1
        else:
            start = 7
            end = 0
            advance = -1

        for i in range (0, 8):
            if self.board[i][start] == "-":
                total_holes += 1
            if self.board[i][start+advance] == "-":
                total_holes += 1

            if self.board[i][end] == team.color:
                total_winning += 1

            if self.board[i][end-advance] == team.color:
                total_almost_winning += 1

            for j in range (0, 8):
                if self.board[i][j] == team.color:
                    total_dispersion += start + j*advance
                    if is_in_bounds(i, j+advance) and self.board[i][j+advance] == "-":
                        total_moves += 1

                    if is_in_bounds(i+1, j+advance) and self.board[i+1][j+advance] != team.color:
                        total_moves += 1
                        if self.board[i+1][j+advance] != "-":
                            total_attack += 1

                    if is_in_bounds(i-1, j+advance) and self.board[i-1][j+advance] != team.color:
                        total_moves += 1
                        if self.board[i-1][j+advance] != "-":
                            total_attack += 1

                    if is_in_bounds(i+1, j+advance) and self.board[i+1][j+advance] == team.color:
                        total_defence += 1

                    if is_in_bounds(i-1, j+advance) and self.board[i-1][j+advance] == team.color:
                        total_defence += 1


        heuristic = total_holes * holes_weight
        heuristic += total_winning * winning_weight
        heuristic += total_almost_winning * almost_winning_weight
        heuristic += total_attack * attack_weight
        heuristic += total_defence * defence_weight
        heuristic += total_moves * moves_weight

        return heuristic

def main():
    # print "Test 1"
    # game = Game("minmax", "random", "aggresive", "none")
    # game.play()
    # print "Test 2"
    # game = Game("alphabeta", "random", "aggresive", "none")
    # game.play()
    # print "Test 3"
    # game = Game("minmax", "random", "defensive", "none")
    # game.play()
    # print "Test 4"
    # game = Game("alphabeta", "random", "defensive", "none")
    # game.play()


    print "Game 1"
    game = Game("minmax", "minmax", "aggresive", "defensive")
    game.play()
    print "Game 2"
    game = Game("alphabeta", "alphabeta", "defensive", "agressive")
    game.play()
    print "Game 3"
    game = Game("minmax", "alphabeta", "aggresive", "agressive")
    game.play()
    print "Game 4"
    game = Game("alphabeta", "minmax", "defensive", "defensive")
    game.play()


if  __name__ =='__main__':main()
