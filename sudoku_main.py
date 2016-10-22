import sudoku

def run_sudoku(gridfile, wordfile):
    s = sudoku.Sudoku()
    s.init(gridfile, wordfile)

    s.solve_grid()


    #cost, expanded = m.find(strategy)
    #print '------------------------------'
    #print 'The strategy evaluated was:', strategy
    #print 'The file evaluated was:', filename
    #print 'The cost of the search was:', cost
    #print 'The expanded cost of the search was:', expanded
    #print '------------------------------'

    #m.output_file(filename +'_'+ strategy +'.txt')

if __name__ == '__main__':
    run_sudoku('gridtest.txt', 'banktest.txt')
    #run_sudoku('grid1.txt', 'bank1.txt')
    #run_sudoku('grid2.txt', 'bank2.txt')
