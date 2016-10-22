import re
import operator
import random
import copy 
import time

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

    def init_grid(self, gridpath):
        self.grid = []
        f = open(gridpath, 'r')
        j = 0
        for line in f:
            row = []
            self.length = len(line)
            for i in range (0, self.length):
                row.append(line[i].lower())
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


    


    #----------------- State checking Functions ----------------------#



    #ensure unique characters for all rows, columns, blocks
    def check_gridstate_valid(self, grid, words):
        empty_count = 0
        numchars = sum(len(s) for s in words)
    	#for all columns + rows
        for x in range(0, 9):
            seen_col = {}
            seen_row = {}
            for y in range(0, 9):
                if grid[x][y] == '_':
                    empty_count += 1

                if grid[x][y] != '_' and grid[x][y] in seen_col:
                    return False
                elif grid[x][y] != '_':
                    seen_col[grid[x][y]] = True

                if grid[y][x] != '_' and grid[y][x] in seen_row:
                    return False
                elif grid[y][x] != '_':
                    seen_row[grid[y][x]] = True
        
        if numchars < empty_count:
            return False

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

                        if grid[real_x][real_y] != '_' and grid[real_x][real_y] in seen_b:
                            return False
                        elif grid[real_x][real_y] != '_':
                            seen_b[grid[real_y][real_x]] = True
        return True


    #ensure unique characters for all rows, columns, blocks, if word at spot is added
    def check_future_gridstate_valid(self, grid, word, words, orientation, x, y):
        if x == 3 and y == 8 and orientation == 'h':
            print grid
        valid_placement = True 
        dont_replace = {}
        for i, c in enumerate(word):
            if orientation == "h":
                if grid[x+i][y] == c:
                    dont_replace[i] = True
                elif grid[x+i][y] == "_":
                    grid[x+i][y] = c
                else:
                    dont_replace[i] = True
                    valid_placement = False

            else:
                if grid[x][y+i] == c:
                    dont_replace[i] = True
                elif grid[x][y+i] == "_":
                    grid[x][y+i] = c
                else:
                    dont_replace[i] = True
                    valid_placement = False

        words.remove(word)

        if x == 3 and y == 8 and orientation == 'h':
            print grid
            print valid_placement


        if valid_placement:
            ret = self.check_gridstate_valid(grid, words)

        if x == 3 and y == 8 and orientation == 'h':
            print  ret
        words.append(word)

        for i, c in enumerate(word):
            if orientation == "h":
                if i not in dont_replace:
                    grid[x+i][y] = "_"
            else:
                if i not in dont_replace:
                    grid[x][y+i] = "_"
 
        if not valid_placement:
            return False

        return ret



    #----------------- Getting Placement Functions ----------------------#



    def get_possible_placements(self, word, words, orientation, grid):
        placements = []
        for x in range(0, 10 - len(word)):
            for y in range(0, 9):
                #at a certain x, y value...
                print "checking", x, y, orientation
                for i, c in enumerate(word):
                    if orientation == "h":
                        if self.check_future_gridstate_valid(grid, word, words, orientation, x, y):
                            placements.append( (word, orientation, x, y) )
                    else:
                        if self.check_future_gridstate_valid(grid, word, words, orientation, y, x):
                            placements.append( (word, orientation, y, x) )
        return placements



    #List of all placements, None if one cannot be placed
    def get_placements(self, words, grid):
        placements = []
        for word in words:
            placed = False
            for o in self.orientations:
                #for all possible spaces
                new_placements = self.get_possible_placements(word, words, o, grid)
                if len(new_placements) > 0:
                    placements = placements + new_placements
                    placed = True
            if not placed:
                return None
        return placements


    #----------------- Heuristic Functions ----------------------#


    #least constraining
    def get_heuristic_value(self, word, orientation, x, y, grid):
        #number of other words' letters it uses 
        overlap = 0
        for i, c in enumerate(word):
            if orientation == "h":
                if grid[x+i][y] != "_":
                    overlap += 1
            else:
                if grid[x][y+1] != "_":
                    overlap += 1

        return overlap

    def create_heuristic_map(self, placements, grid):
        heuristic_vals = {}
        for placement in placements:
            hval = self.get_heuristic_value(placement[0], placement[1], placement[2], placement[3], grid)
            heuristic_vals[(placement[0], placement[1], placement[2], placement[3])] = hval
        return heuristic_vals



    def create_word_frequency_map(self, possible_moves):
        seen_words = {}
        for move in possible_moves:
            if move[0] not in seen_words:
                seen_words[move[0]] = 1
            else:
                seen_words[move[0]] += 1
        return seen_words



    def sorted_by_heuristic(self, placements, words, grid):
        heuristic_map = self.create_heuristic_map(placements, grid)
        frequency_map = self.create_word_frequency_map(placements)
        sorted_moves = []
        for move in placements:
            sorted_moves.append( (move[0], move[1], move[2], move[3], frequency_map[move[0]], heuristic_map[move] ) )

        #sort by heuristic vals
        sorted_moves = sorted(sorted_moves, key=lambda x: (x[4], -x[5]))

        ret_moves = []
        for move in sorted_moves:
            ret_moves.append( (move[0], move[1], move[2], move[3]) )

        return ret_moves



    #----------------- Filtering Functions ----------------------#



    def filter_by_valid_placement(self, moves, grid, words):
        valid_moves = []
        for move in moves:
            if self.check_future_gridstate_valid(grid, move[0], words, move[1], move[2], move[3]):
                if move not in valid_moves: 
                    valid_moves.append(move)
        return valid_moves


    #----------------- Solve helper Functions ----------------------#




    def solved_state(self, grid, words):
        if len(words) == 0:
            for col in grid:
                if "_" in col:
                    return False
            return True
        else:
            return False



    #----------------- Main Functions ----------------------#

    def solve_copy(self, grid, words, placements, move):
        word = move[0]
        orientation = move[1]
        x = move[2]
        y = move[3]

        #add word to grid
        dont_replace = {}
        for i, c in enumerate(word):
            if orientation == "h":
                if grid[x+i][y] == c:
                    dont_replace[i] = True
                elif grid[x+i][y] == '_':
                    grid[x+i][y] = c
                elif i == 0:
                    raise ValueError('Tried to place a letter where another existed already')
            else:
                if grid[x][y+i] == c:
                    dont_replace[i] = True
                elif grid[x][y+i] == '_':
                    grid[x][y+i] = c
                elif i == 0:
                    raise ValueError('Tried to place a letter where another existed already')

        words.remove(word)

        #remove placement from placements
        valid_placements = []
        for placement in placements:
            if placement[0] != word:
                valid_placements.append(placement)
        
        #remove invalid placements from placements
        valid_placements = self.filter_by_valid_placement(valid_placements, grid, words)

        solved = self.solve(words, grid, valid_placements)

        if solved[1] > 70000:
            print "70K ANALYSIS....."
            print grid
            print words
            print move
            print "......"

        words.append(word)

        for i, c in enumerate(word):
            if orientation == "h":
                if i not in dont_replace:
                    grid[x+i][y] = "_"
            else:
                if i not in dont_replace:
                    grid[x][y+i] = "_"

        return solved



    def solve(self, words, grid, placements):
        #if not self.check_gridstate_valid(grid):
        #    return (False, 0)
        if self.solved_state(grid, words):
            print "---------Solved----------"
            print grid
            return (True, 0)

        #pass down hash words -> list of all possible moves for that word
        #just eliminate invalid ones here

        if placements == None: #if a future placement is not possible
            return (False, 0)
        if len(placements) == 0: #no current overlapping placement
            return (False, 0)

        sorted_moves = self.sorted_by_heuristic(placements, words, grid)

        #print len(sorted_moves)

        expanded = 1
        for i, move in enumerate(sorted_moves):
            if i > 5: #193 seconds for 4
                break
             
            solved = self.solve_copy( grid, words, placements, move)
            if solved[1] > 70000:
                print "SORTED EXPANDS MORE THAN 70k"
                print move

            expanded += solved[1]
            if solved[0]:
                return (True, expanded)
            
        if expanded > 10000:
            #if expanded > 70000:
            #    print placements
            print expanded
            print grid
            print words

        return (False, expanded)

    #helper function called externally
    def solve_grid(self):
        start_time = time.time()
        placements = self.get_placements(self.words, self.grid)
        print placements
        placements = self.filter_by_valid_placement(placements, self.grid, self.words)

        runtime = (time.time() - start_time) 
        print "starting placement amount:"
        print len(placements)
        print self.solve(self.words, self.grid, placements)

        runtime = (time.time() - start_time) 
        print "finished in "
        print runtime
        print "seconds"



