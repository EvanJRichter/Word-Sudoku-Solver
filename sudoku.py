import re

class Sudoku:
    original = []
    height = -1
    length = -1
    #Assumptions: Grid will always be 9x9
    grid = []
    words = []

    def init(self, gridpath, wordpath):
        self.init_grid(gridpath)
        self.init_words(wordpath)

        print self.grid
        print self.words

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

    

    #get heuristic val


    #ensure unique characters for all rows, columns, blocks
    def check_gridstate_valid(self):
    	#for all columns
        for x in range(0, 9):
            seen_col = {}
            seen_row = {}
            for y in range(0, 9):
                if self.grid[x][y] != '_' and self.grid[x][y] in seen_col:
                    print self.grid[x][y] 
                    return False
                else:
                    seen_col[self.grid[x][y]] = True

                if self.grid[y][x] != '_' and self.grid[y][x] in seen_row:
                    return False
                else:
                    seen_row[self.grid[y][x]] = True

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
                            self.grid[real_y][real_x] = True

        return True


    def solved_state(self):
        return True


    def solve(self):
        if not self.check_gridstate_valid():
            print "INVALID"
            return False
        if self.solved_state():
            print "Solved!!!!"
            return True

        #go through remaining words
            #for either orientation
                #for all possible spaces
                    #get + save heuristic val for space

        #sort heuristic vals
        #go through heuristic vals from best to worst
            #val = recurse(with updated board)
            #if val:
                #return true
            
        #return false





