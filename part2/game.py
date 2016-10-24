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
        count = 0
        while not self.is_game_over() or count < 10:
            self.move()
            self.alternate_turn()
            self.print_game()
            count += 1
        return

    def print_game(self):
        board = ""
        for i in range (0, 8):
            for j in range (0, 8):
                board += self.board[i][j] + "|"
            board +=  "\n"
            board += "_ _ _ _ _ _ _ _"
            board += "\n"
        print board

    def move(self):
        move = self.minmax_decision()
        self.do_move(move[0], move[1])

    def alternate_turn(self):
        if self.turn == self.white:
            self.turn = self.black
            self.opponent = self.white
        else:
            self.turn = self.white
            self.opponent = self.black

    def touchdown(self):
        for i in range (0, 8):
            if self.board[i][0] == "b" or self.board[i][7] == "w":
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
        for move in possible_moves:
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
            prev = self.do_move(move[0], move[1])
            value, useless_move = self.max_value(level + 1)
            if value <= min_value :
                min_value = value
                min_move = move
            self.undo_move(move[0], move[1], prev)
        return min_value, min_move

    def evaluate_board(self):
        total_holes = 0
        total_winning = 0
        total_almost_winning = 0
        total_attack = 0
        total_defence = 0
        total_moves = 0
        total_dispersion = 0

        holes_weight = 0
        winning_weight = 0
        almost_winning_weight = 0
        attack_weight = 0
        defence_weight = 0
        moves_weight = 0
        dispersion_weight = 0

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

        for i in range (0, 8):
            if self.board[i][start] == "-":
                total_holes += 1
            if self.board[i][start+advance] == "-":
                total_holes += 1

            if self.board[i][end] == self.turn.color:
                total_winning += 1

            if self.board[i][end-advance] == self.turn.color:
                total_almost_winning += 1

            for j in range (0, 8):
                if self.board[i][j] == self.turn.color:
                    total_dispersion += start + j*advance
                    if is_in_bounds(i, j+advance) and self.board[i][j+advance] == "-":
                        total_moves += 1

                    if is_in_bounds(i+1, j+advance) and self.board[i+1][j+advance] != self.turn.color:
                        total_moves += 1
                        if self.board[i+1][j+advance] != "-":
                            total_attack += 1

                    if is_in_bounds(i-1, j+advance) and self.board[i-1][j+advance] != self.turn.color:
                        total_moves += 1
                        if self.board[i-1][j+advance] != "-":
                            total_attack += 1

                    if is_in_bounds(i+1, j+advance) and self.board[i+1][j+advance] == self.turn.color:
                        total_defence += 1

                    if is_in_bounds(i-1, j+advance) and self.board[i-1][j+advance] == self.turn.color:
                        total_defence += 1

        if self.turn.heuristic == "aggresive":
            holes_weight = 0 # Defensive
            winning_weight = 20 # Aggresive
            almost_winning_weight = 10 # Aggresive
            attack_weight = 10 # Aggresive
            defence_weight = 5 # Defensive
            moves_weight = 5 # Equal
            dispersion_weight = 10 # Aggresive
        else:
            holes_weight = -10
            winning_weight = 5
            almost_winning_weight = 5
            attack_weight = 5
            defence_weight = 20
            moves_weight = 5
            dispersion_weight = -10


        heuristic = total_holes * holes_weight
        heuristic += total_winning * winning_weight
        heuristic += total_almost_winning * almost_winning_weight
        heuristic += total_attack * attack_weight
        heuristic += total_defence * defence_weight
        heuristic += total_moves * moves_weight

        return heuristic

def main():
    game = Game("minmax", "minmax", "aggresive", "agressive")
    game.play()


if  __name__ =='__main__':main()
