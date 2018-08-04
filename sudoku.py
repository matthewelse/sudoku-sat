import numpy as np

from box import box_chars


class Sudoku:
    """
    Class to represent a sudoku puzzle.
    """

    def __init__(self, size, box_width, box_height):
        assert box_width * box_height == size

        self.grid = np.zeros((size, size), dtype=np.uint8)
        self.size = size
        self.box_width, self.box_height = box_width, box_height

    @classmethod
    def of_string(cls, sudoku, size = 9, box_width = 3, box_height = 3):
        assert size * size == len(sudoku)
        assert box_width * box_height == size

        if len(sudoku) == 81:
            puzzle = cls(size, box_width, box_height)

            for i, c in enumerate(sudoku):
                x, y = divmod(i, size)

                puzzle.grid[x, y] = 0 if c == '.' else int(c)

            return puzzle
        else:
            assert False, "Invalid size of sudoku puzzle."

    def complete(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] < 1 or self.grid[i, j] > self.size:
                    # incomplete
                    return False

        return True

    def solved(self):
        if not self.complete():
            return False

        # we know it's complete, check whether it's correct
        # columns
        for i in range(self.size):
            if len(set(self.grid[:, i])) != self.size:
                print('bad column %i' % i)
                return False

        # rows
        for j in range(self.size):
            if len(set(self.grid[j])) != self.size:
                print('bad row %i' % i)
                return False

        # sub-grids
        for i in range(self.box_width):
            for j in range(self.box_height):
                start_x = j * self.box_width
                start_y = i * self.box_height

                sub_grid = self.grid[start_x:start_x+self.box_width,
                                     start_y:start_y+self.box_height]

                if len(set(sub_grid.flatten())) != self.size:
                    print('bad sub-grid %i, %i' % (i, j))
                    return False

        return True

    def specified(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] != 0:
                    yield (i, j, self.grid[i, j])

    def _box_border(self, divider, left, right, spacer):
        spacer_width = self.box_width * 2 + 1
        result = spacer * spacer_width
        result = divider.join(result for i in range(self.box_height))

        return left + result + right

    def _box_inner_row(self, j):
        # split into box_height parts (each is box_width)
        parts = np.split(self.grid[j], self.box_height)

        chunks = (' ' + ' '.join(
            str(x) if x != 0 else ' ' for x in part
        ) + ' ' for part in parts)

        return box_chars['b|'] + box_chars['|'].join(chunks) + box_chars['b|']

    def _box_row(self, i):
        """
        Print a chunk of rows: box_height rows joined by \n.
        """
        return '\n'.join(
            self._box_inner_row(i * self.box_height + j) for j in range(self.box_height)
        )

    def __str__(self):
        inter_width = self.box_width * 2 + 1

        header = self._box_border(
            box_chars['T'],
            box_chars['uL'],
            box_chars['xL'],
            box_chars['b-'])
        footer = self._box_border(
            box_chars['uT'],
            box_chars['L'],
            box_chars['rL'],
            box_chars['b-'])
        middle = '\n' + self._box_border(
            box_chars['+'],
            box_chars['l+'],
            box_chars['r+'],
            box_chars['-']) + '\n'

        body = middle.join(self._box_row(i) for i in range(self.box_width))

        return '\n'.join([
            header,
            body,
            footer
        ])
