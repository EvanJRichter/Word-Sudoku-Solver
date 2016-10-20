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
        self.grid = zip(*self.grid)
        self.grid = [list(row) for row in self.grid]


    def init_words(self, wordpath):
        f = open(wordpath, 'r')
        text = f.read()
        f.close()
        self.words = list(text.split())

    def solve(self):
        if !check_gridstate_valid():
            return False
        if solved_state():
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






        #get heuristic val


        #checks if grid 
        def check_gridstate_valid():
        	#for all rows
        		#ensure unique
        	#for all columns
        		#ensure unique
            #for all blocks
                #ensure unique
            return True









