
    #least constraining
    def get_heuristic_value(self, word, orientation, x, y, grid):
        #in the fewest rows, columns, blocks 
        #in_blocks = (len(word)-1) / 3
        #in_cells = len(word)

        #return -1 * (in_blocks + in_cells)

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

        #openness of blocks, rows, cols
        openval = 0
        for i in range(0, 9):
            colval = 0
            rowval = 0
            for k in range(0, 9):
                if self.will_cell_be_full(word, orientation, grid, x, y, i, k):
                    colval += 1
                if self.will_cell_be_full(word, orientation, grid, x, y, k, i):
                    rowval += 1
            openval += colval + rowval


        #For all blocks
        for x_b in range(0, 3):
            for y_b in range(0, 3):
                blockval = 0
                offset_x = x_b * 3
                offset_y = y_b * 3
                for x in range(0, 3):
                    for y in range(0, 3):
                        real_x = offset_x + x
                        real_y = offset_y + y

                        if self.will_cell_be_full(word, orientation, grid, x, y, real_x, real_y):
                            blockval += 1
                openval += blockval

        return (openval + overlap) - (in_blocks + in_cells)

    def will_cell_be_full(self, word, orientation, grid, word_x, word_y, x, y):
        if grid[x][y] != "_":
            return True
        if orientation == "h":
            if word_x <= x and x <= word_x+len(word) and word_y == y: #off by one maybe? 
                return True
        else:
            if word_y <= y and y <= word_y+len(word) and word_x == x: #off by one maybe? 
                return True
        return False
