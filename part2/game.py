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

    def move():
        locationA, locationB = choose_best_move()
        perform_move(locationA, locationB)

    def generate_possible_moves(temp_board):

    def choose_best_move():


    def perform_move(locationA, locationB):
        self.board.updatePiece(locationA, locationB)

    def alternate_turn():
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

    def get_possible_boards(temp_board):
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

        possible_boards = []

        for i in range (0, 8):
            for j in range (0, 8):
                if temp_board[i][j] == self.turn.color:
                    if is_in_bounds(i, j + advance) and temp_board[i][j + advance] == "-":
                        new_board = temp_board
                        new_board = update_board(new_board, (i, j), (i, j + advance))
                        locationA = (i, j)
                        locationB = (i, j + advance)
                        possible_boards.append((new_board, locationA, locationB))

                    if is_in_bounds(i + 1, j + advance) and temp_board[i + 1][j + advance] != self.turn.color:
                        new_board = temp_board
                        new_board = update_board(new_board, (i, j), (i, j + advance))
                        locationA = (i, j)
                        locationB = (i + 1, j + advance)
                        possible_boards.append((new_board, locationA, locationB))

                    if is_in_bounds(i - 1, j+advance) and temp_board[i - 1][j + advance] != self.turn.color:
                        new_board = temp_board
                        new_board = update_board(new_board, (i, j), (i, j + advance))
                        locationA = (i, j)
                        locationB = (i - 1, j + advance)
                        possible_boards.append((new_board, locationA, locationB))

        return possible_boards

    def update_piece(board, locationA, locationB):
        board[locationB.first][locationB.second] = self.board[locationA.first][locationA.second]
        board[locationA.first][locationA.second] = "-"
        return board

    def minmax_decision(temp_board):
        v = max_value(temp_board, 0)
        possible_boards = get_possible_boards(temp_board)

        return #TODO how the fuck do you identify the move that had such value

    def max_value(temp_board, level):
        if level == 3:
            return evalute_board(temp_board)

        possible_boards = get_possible_boards(temp_board)
        if possible_boards is empty:
            return evalute_board(temp_board)

        v = -INFINITE

        for board in possible_boards:
            v = max (v, min_value(board, level + 1))
        return v

    def max_value(temp_board, level):
        if level == 3:
            return evalute_board(temp_board)

        possible_boards = get_possible_boards(temp_board)
        if possible_boards is empty:
            return evalute_board(temp_board)

        v = -INFINITE #TODO

        for board in possible_boards:
            v = min(v, max_value(board, level + 1))
        return v

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
