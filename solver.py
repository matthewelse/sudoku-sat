from functools import reduce
from operator import and_, or_

from satispy import Variable, Cnf
from sudoku import Sudoku

def exactly_one(expressions):
    expressions = list(expressions)

    def inner():
        for i, e1 in enumerate(expressions):
            for j, e2 in enumerate(expressions):
                if i == j:
                    continue

                yield -e1 | -e2


    return reduce(and_, inner()) & reduce(or_, expressions)

def box(i, j, k):
    return Variable('s_%d_%d_%d' % (i, j, k))

def known(puzzle):
    return reduce(and_, (box(i, j, k) for i, j, k in puzzle.specified()))

def all_boxes_rule(puzzle):
    # all boxes have exactly one number
    expressions = (
        exactly_one(box(row, col, value) for value in range(1, puzzle.size + 1))
        for row in range(puzzle.size)
        for col in range(puzzle.size)
        )

    return reduce(and_, expressions)

def row_rule(puzzle):
    expressions = (
            exactly_one(box(row, col, value) for col in range(puzzle.size))
        
            for row in range(puzzle.size)
            for value in range(1, puzzle.size + 1)
        )

    return reduce(and_, expressions)

def column_rule(puzzle):
    expressions = (
            exactly_one(box(row, col, value) for row in range(puzzle.size))
        
            for col in range(puzzle.size)
            for value in range(1, puzzle.size + 1)
        )

    return reduce(and_, expressions)

def sub_grid_rule(puzzle):
    def inner(i, j, z):
        x0 = i * puzzle.box_width
        y0 = j * puzzle.box_height

        for dx in range(puzzle.box_width):
            for dy in range(puzzle.box_height):
                yield box(x0 + dx, y0 + dy, z)

    def inner_2():
        for i in range(puzzle.box_height):
            for j in range(puzzle.box_width):
                for z in range(1, puzzle.size + 1):
                    yield exactly_one(inner(i, j, z))

    return reduce(and_, inner_2())

def of_binary(solution, size = 9, box_width = 3, box_height = 3):
    puzzle = Sudoku(size, box_width, box_height)

    for i in range(size):
        for j in range(size):
            for k in range(1, size + 1):
                var = box(i, j, k)
                if var in solution.varmap and solution[var]:
                    puzzle.grid[i, j] = k
                    break

    return puzzle
