class Player:
    self.color = None
    self.strategy = None
    self.heuristic = None
    self.pieces = None
    self.count = None

    def Player(self, color, strategy, heuristic):
        self.color = color
        self.strategy = strategy
        self.heuristic = heuristic
        self.count = 16

class Game:
    self.board = None
    self.white = None
    self.black = None
    self.turn = None
    self.opponent = None

    def Game(self, sw, sb, hw, hb):
        self.board = []
        for i in range (0, 8):
            self.array[i] = []
            for j in range (0, 8):
                self.board[i][j] = "-"

        for i in range (0, 8):
            self.board[i][0] = "w"
            self.board[i][1] = "w"
            self.board[i][6] = "b"
            self.board[i][7] = "b"

        self.white = Player("w", sw, hw)
        self.black = Player("b", sb, hb)
        self.turn = white
        self.opponent = black

    def play(self):
        while !is_game_over():
            move()
            alternate_turn()
        print self.board
        return

    def move(self):
        move = minmax_decision()
        self.board = do_move(self.board, move[0], move[1])

    def alternate_turn(self):
        if self.turn == white:
            self.turn = black
            self.opponent = white
        else:
            self.turn = white
            self.opponent = black

    def is_game_over(self):
        if white.count == 0 or black.count == 0 or board.touchdown():
            return True
        return False

    def get_possible_moves(temp_board):
        start = -1
        end = -1
        advance = 0

        if self.turn = white:
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
                if temp_board[i][j] == self.turn.color:
                    if is_in_bounds(i, j + advance) and temp_board[i][j + advance] == "-":
                        locationA = (i, j)
                        locationB = (i, j + advance)
                        possible_moves.append((locationA, locationB))

                    if is_in_bounds(i + 1, j + advance) and temp_board[i + 1][j + advance] != self.turn.color:
                        locationA = (i, j)
                        locationB = (i + 1, j + advance)
                        possible_moves.append((locationA, locationB))

                    if is_in_bounds(i - 1, j+advance) and temp_board[i - 1][j + advance] != self.turn.color:
                        locationA = (i, j)
                        locationB = (i - 1, j + advance)
                        possible_moves.append((locationA, locationB))

        return possible_moves

    def do_move(board, locationA, locationB):
        if board[locationB.first][locationB.second] == "w":
            self
        prev = board[locationB.first][locationB.second]
        board[locationB.first][locationB.second] = self.board[locationA.first][locationA.second]
        board[locationA.first][locationA.second] = "-"
        return (board, prev)

    def undo_move(board, locationA, locationB, prev):
        board[locationA.first][locationA.second] = board[locationB.first][locationB.second]
        board[locationB.first][locationB.second] = prev
        return board

    def minmax_decision(self):
        value, move = max_value(self.board, 0)
        return move

    def max_value(temp_board, level):
        if level == 3:
            return (evalute_board(temp_board), None)

        possible_moves = get_possible_moves(temp_board)
        if possible_moves is empty:
            return (evalute_board(temp_board), None)

        max_value = -float("inf")
        max_move = None
        for move in possible_moves:
            temp_board, prev = do_move(board, move[0], move[1])
            value, useless_move = min_value(board, level + 1)
            if value >= max_value :
                max_value = value
                max_move = move
            temp_board = undo_move(board, move[0], move[1], prev)
        return max_value, max_move

    def min_value(temp_board, level):
        if level == 3:
            return (evalute_board(temp_board), None)

        possible_moves = get_possible_moves(temp_board)
        if possible_moves is empty:
            return (evalute_board(temp_board), None)

        min_value = float("inf")
        min_move = None
        for move in possible_moves:
            temp_board, prev = do_move(board, move[0], move[1])
            value, useless_move = min_value(board, level + 1)
            if value <= max_value :
                min_value = value
                min_move = move
            temp_board = undo_move(board, move[0], move[1], prev)
        return min_value, min_move

    def is_in_bounds(x, y):
        if x >= 0 and x < 8 and y >= 0 and  y < 8:
            return True
        return False

    def evaluate_board(temp_board):
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
        if self.turn = white:
            start = 0
            end = 7
            advance = 1
        else:
            start = 7
            end = 0
            advance = -1

        for i in range (0, 8):
            if temp_board[i][start] == "-":
                total_holes += 1
            if temp_board[i][start+advance] == "-":
                total_holes += 1

            if temp_board[i][end] == self.turn.color:
                total_winning += 1

            if temp_board[i][end-advance] == self.turn.color:
                total_almost_winning += 1

            for j in range (0, 8):
                if temp_board[i][j] == self.turn.color:
                    total_dispersion += start + j*advance
                    if is_in_bounds(i, j+advance) and temp_board[i][j+advance] == "-":
                        total_moves += 1

                    if is_in_bounds(i+1, j+advance) and temp_board[i+1][j+advance] != self.turn.color:
                        total_moves += 1
                        if temp_board[i+1][j+advance] != "-":
                            total_attacks += 1

                    if is_in_bounds(i-1, j+advance) and temp_board[i-1][j+advance] != self.turn.color:
                        total_moves += 1
                        if temp_board[i-1][j+advance] != "-":
                            total_attacks += 1

                    if is_in_bounds(i+1, j+advance) and temp_board[i+1][j+advance] == self.turn.color:
                        total_defence += 1

                    if is_in_bounds(i-1, j+advance) and temp_board[i-1][j+advance] == self.turn.color:
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
