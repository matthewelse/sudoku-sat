import sys

from functools import reduce
from operator import or_, and_

import numpy as np

from satispy.solver import Minisat

from sudoku import Sudoku
from solver import *

# Solving sudoku puzzles using a sat solver:
# see https://pdfs.semanticscholar.org/535d/06391275618a7b913d1c98a1353286db8d74.pdf

example = sys.argv[1]

grid = Sudoku.of_string(example)

print(grid)

expr = row_rule(grid) & column_rule(grid) & known(grid) & all_boxes_rule(grid) & sub_grid_rule(grid)

solver = Minisat()
solution = solver.solve(expr)

if solution.success:
    print('satisfiable')
    result = of_binary(solution)
    print(result)

    if result.solved():
        print('solved successfully')
else:
    print('not satisfiable')
