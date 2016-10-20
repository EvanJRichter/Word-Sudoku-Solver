import re
import operator
import random
import copy 

class Sudoku:
    original = []
    height = -1
    length = -1
    #Assumptions: Grid will always be 9x9
    grid = []
    words = []
    orientations = ['h', 'v']

    def init(self, gridpath, wordpath):
        self.init_grid(gridpath)
        self.init_words(wordpath)

        #print self.grid
        #print self.words

    def init_grid(self, gridpath):
        self.grid = []
        f = open(gridpath, 'r')
        j = 0
        for line in f:
            row = []
            self.length = len(line)
            for i in range (0, self.length):
                row.append(line[i])
            self.grid.append(row)
            j += 1
        f.close()

        self.height = j
        #arrange it to how I think about it in my head (grid[x][y])
        self.grid = zip(*self.grid)
        self.grid = [list(row) for row in self.grid]


    def init_words(self, wordpath):
        f = open(wordpath, 'r')
        text = f.read()
        f.close()
        self.words = list(text.split())

    

    #ensure unique characters for all rows, columns, blocks
    def check_gridstate_valid(self):
    	#for all columns + rows
        for x in range(0, 9):
            seen_col = {}
            seen_row = {}
            for y in range(0, 9):
                if self.grid[x][y] != '_' and self.grid[x][y] in seen_col:
                    return False
                else:
                    seen_col[self.grid[x][y]] = True

                if self.grid[y][x] != '_' and self.grid[y][x] in seen_row:
                    return False
                else:
                    seen_row[self.grid[y][x]] = True

        #For all blocks
        for x_b in range(0, 3):
            for y_b in range(0, 3):
                offset_x = x_b * 3
                offset_y = y_b * 3
                seen_b = {}
                for x in range(0, 3):
                    for y in range(0, 3):
                        real_x = offset_x + x
                        real_y = offset_y + y

                        if  self.grid[real_x][real_y] != '_' and self.grid[real_x][real_y] in seen_col:
                            return False
                        else:
                            seen_b[self.grid[real_y][real_x]] = True

        return True


    def solved_state(self, words):
        if len(words) == 0:
            return True
        return False

    def get_possible_placements(self, word, orientation, grid):
        placements = []
        for x in range(0, 9 - len(word)):
            for y in range(0, 9 - len(word)):
                #at a certain x, y value...
                valid = True
                for i, c in enumerate(word):
                    if orientation == "h":
                        if grid[x+i][y] != "_" and grid[x+i][y] != "c":
                            valid = False
                            break
                    if orientation == "v":
                        if grid[x][y+i] != "_" and grid[x][y+i] != "c":
                            valid = False
                            break
                if valid:
                    placements.append((x, y))
        return placements


    #TODO: get heuristic val
    def get_heuristic_value(self, word, orientation, x, y, grid):
        return 1



    def solve(self, words, grid):
        if not self.check_gridstate_valid():
            print "INVALID"
            return False
        if self.solved_state(words):
            print "Solved!!!!"
            print grid
            return True

        #map from (word, orientation, x, y) to heuristic value
        heuristic_vals = {}
        #go through remaining words
        for word in words:
            for o in self.orientations:
                #for all possible spaces
                for placement in self.get_possible_placements(word, o, grid):
                    hval = self.get_heuristic_value(word, o, placement[0], placement[1], grid)
                    heuristic_vals[(word, o, placement[0], placement[1])] = hval

        #sort by heuristic vals
        sorted_moves = sorted(heuristic_vals.items(), key=operator.itemgetter(1), reverse=True)
        #go through moves from best to worst
        for move in sorted_moves:
            #create updated board
            new_grid = copy.deepcopy(grid)
            for i, c in enumerate(move[0][0]):
                if move[0][1] == 'h':
                    new_grid[move[0][2] + i][move[0][3]] = c
                else:    
                    new_grid[move[0][2]][move[0][3] + i] = c

            #create updated word list
            new_words = copy.deepcopy(words)
            new_words.remove(move[0][0])

            success = self.solve(new_words, new_grid)
            if success:
                return True
            
        return False

    #helper function called externally
    def solve_grid(self):
        if self.solve(self.words, self.grid):
            print "wahoo!!!!"



