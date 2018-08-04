import sys
from sudoku import Sudoku

puzzle = Sudoku.of_string(sys.argv[1])
print(puzzle)

