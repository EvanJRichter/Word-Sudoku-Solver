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

    

    #ensure unique characters for all rows, columns, blocks
    def check_gridstate_valid(self, grid):
    	#for all columns + rows
        for x in range(0, 9):
            seen_col = {}
            seen_row = {}
            for y in range(0, 9):
                if grid[x][y] != '_' and grid[x][y] in seen_col:
                    return False
                else:
                    seen_col[grid[x][y]] = True

                if grid[y][x] != '_' and grid[y][x] in seen_row:
                    return False
                else:
                    seen_row[grid[y][x]] = True

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

                        if grid[real_x][real_y] != '_' and grid[real_x][real_y] in seen_col:
                            return False
                        else:
                            seen_b[grid[real_y][real_x]] = True

        return True


    #ensure unique characters for all rows, columns, blocks, if word at spot is added
    def check_future_gridstate_valid(self, grid, word, orientation, x, y):
        dont_replace = {}
        for i, c in enumerate(word):
            if orientation == "h":
                if grid[x+i][y] != "_":
                    dont_replace[i] = True
                else:
                    grid[x+i][y] = c
            else:
                if grid[x][y+i] != "_":
                    dont_replace[i] = True
                else:
                    grid[x][y+i] = c

        ret = self.check_gridstate_valid(grid)

        for i, c in enumerate(word):
            if orientation == "h":
                if i not in dont_replace:
                    grid[x+i][y] = "_"
            else:
                if i not in dont_replace:
                    grid[x][y+i] = "_"

        return ret




    def get_possible_placements(self, word, orientation, grid):
        placements = []
        for x in range(0, 10 - len(word)):
            for y in range(0, 9):
                #at a certain x, y value...
                valid = True
                foundchar = False
                for i, c in enumerate(word):
                    if orientation == "h":
                        if grid[x+i][y] != "_" and grid[x+i][y] != c:
                            valid = False
                            break
                        if grid[x+i][y] == c:
                            foundchar = True
                    else:
                        if grid[y][x+i] != "_" and grid[y][x+i] != c:
                            valid = False
                            break
                        if grid[y][x+i] == c:
                            foundchar = True
                if valid and foundchar:
                    if orientation == "h":
                        placements.append( (word, orientation, x, y) )
                    else:
                        placements.append( (word, orientation, y, x) )
                       
        return placements

    def could_be_placed(self, word, orientation, grid):
        for x in range(0, 10 - len(word)):
            for y in range(0, 9):
                valid = True
                for i, c in enumerate(word):
                    if orientation == "h":
                        if grid[x+i][y] != "_" and grid[x+i][y] != c:
                            valid = False
                            break
                    if orientation == "v":
                        if grid[y][x+i] != "_" and grid[y][x+i] != c:
                            valid = False
                            break
                if valid:
                    return True
        return False


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

    def sorted_by_heuristic(self, placements, grid):
        heuristic_map = self.create_heuristic_map(placements, grid)        

        #sort by heuristic vals
        sorted_moves = sorted(heuristic_map.items(), key=operator.itemgetter(1), reverse=True)
        if len(sorted_moves) == 0:
            return (False, 0)
        sorted_moves = [i[0] for i in sorted_moves] #strip heuristics
        return sorted_moves


    #List of all placements, None if one cannot be placed
    def get_placements(self, words, grid):
        placements = []
        for word in words:
            placed = False
            for o in self.orientations:
                #for all possible spaces
                new_placements = self.get_possible_placements(word, o, grid)
                if len(new_placements) > 0:
                    placements = placements + new_placements
                    placed = True
                if not placed:
                    placed = self.could_be_placed(word, o, grid)
            if not placed:
                return None
        return placements

    def filter_by_unique_moves(self, possible_moves):
        #get many can be placed
        seen_words = {}
        for move in possible_moves:
            if move[0] not in seen_words:
                seen_words[move[0]] = 1
            else:
                seen_words[move[0]] += 1

        unique_moves = []
        for move in possible_moves:
            if seen_words[move[0]] == 1:
                unique_moves.append(move)

        return unique_moves

    def filter_by_valid_future(self, moves, grid):
        valid_moves = []
        for move in moves:
            if self.check_future_gridstate_valid(grid, move[0], move[1], move[2], move[3]):
                valid_moves.append(move)
        return valid_moves

    def get_updated_grid(self, grid, move):
        new_grid = copy.deepcopy(grid)
        for i, c in enumerate(move[0]):
            if move[1] == 'h':
                new_grid[move[2] + i][move[3]] = c
            else:    
                new_grid[move[2]][move[3] + i] = c
        return new_grid

    def solved_state(self, grid, words):
        if len(words) == 0:
            return True
        for col in grid:
            if "_" in col:
                return False
        return True

    def solve(self, words, grid):
        #if not self.check_gridstate_valid(grid):
        #    return (False, 0)
        if self.solved_state(grid, words):
            print "---------Solved----------"
            print grid
            return (True, 0)

        print "placements"
        start_time = time.time()

        possible_moves = self.get_placements(words, grid)
        if possible_moves == None: #if a future placement is not possible
            return False
        if len(possible_moves) == 0: #no current overlapping placement
            return False

        print (time.time() - start_time)


        unique_moves = self.filter_by_unique_moves(possible_moves)
        if len(unique_moves) == 0:
            return (False, 0)

        print "valid"
        start_time = time.time() 

        valid_moves = self.filter_by_valid_future(unique_moves, grid)
        if len(valid_moves) == 0:
            return (False, 0)

        print (time.time() - start_time)


        sorted_moves = self.sorted_by_heuristic(valid_moves, grid)


        #print len(valid_moves) - len(unique_moves)
        #print valid_moves, unique_moves

        expanded = 1
        for i, move in enumerate(sorted_moves):
            if i > 2:
                break

            print "copy"
            start_time = time.time() 

            new_grid = self.get_updated_grid(grid, move)
            new_words = copy.deepcopy(words)
            new_words.remove(move[0])

            print (time.time() - start_time)

            solved = self.solve(new_words, new_grid)

            expanded += solved[1]
            if solved[0]:
                return (True, expanded)
            
        return (False, expanded)

    #helper function called externally
    def solve_grid(self):
        start_time = time.time()
        print self.solve(self.words, self.grid)
        dun = (time.time() - start_time) 
        print "finished in "
        print dun
        print "seconds"



