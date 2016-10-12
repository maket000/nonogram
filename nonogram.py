CHECK_INC = 0
CHECK_FAIL = 1
CHECK_OK = 2

GRID_EMPTY = 0
GRID_FILL = 1
GRID_BLOCK = 2


class Mut:
    def __init__(self, val):
        self.val = val
    def get(self):
        return self.val
    def set(self, val):
        self.val = val


def get_clues(grid): # TODO: make get_clues dimension-ambiguous
    """Produce the row and column clues for a nonogram grid"""
    height = len(grid)
    width = len(grid[0])
    row_clues = [[0] for _ in xrange(height)]
    col_clues = [[0] for _ in xrange(width)]

    for y in xrange(height):
        for x in xrange(width):
            if grid[y][x]:
                if row_clues[y][-1] >= 0:
                    row_clues[y].append(-1)
                else:
                    row_clues[y][-1] -= 1
                if col_clues[x][-1] >= 0:
                    col_clues[x].append(-1)
                else:
                    col_clues[x][-1] -= 1
            else:
                if row_clues[y][-1] < 0:
                    row_clues[y][-1] = -row_clues[y][-1]
                if col_clues[x][-1] < 0:
                    col_clues[x][-1] = -col_clues[x][-1]

    for i in xrange(height):
        if row_clues[i][-1] < 0:
            row_clues[i][-1] = -row_clues[i][-1]
        row_clues[i] = row_clues[i][1:]
    for i in xrange(width):
        if col_clues[i][-1] < 0:
            col_clues[i][-1] = -col_clues[i][-1]
        col_clues[i] = col_clues[i][1:]
    return row_clues, col_clues


def print_grid(grid):
    s = ""
    for y in xrange(len(grid[0])):
        for x in xrange(len(grid[0][0])):
            s += str(grid[0][y][x].get()) + ' '
        s += '\n'
    print s


def insert_range(grid, side, line, first, last):
    for i in xrange(first, last+1):
        grid[side][line][i].set(1)


def check_line(grid, clues, side, line):
    clue_i = 0
    cell_i = 0
    state = CHECK_OK
    while cell_i < len(grid[side][line]):
        if grid[side][line][cell_i] == GRID_FILL:
            if clue_i >= len(clues[side][line]):
                return CHECK_FAIL
            for cell_i in xrange(cell_i+1, cell_i+clues[side][line][clue_i]):
                if grid[side][line][cell_i] != GRID_FILL:
                    state = CHECK_INC
            clue_i += 1
            cell_i += 1
            if (cell_i != len(grid[side][line]) and
                grid[side][line][cell_i] == GRID_FILL):
                return CHECK_FAIL
        else:
            cell_i += 1
    if clue_i < len(clues[side][line]) - 1:
        return CHECK_INC
    return state

def check_all(grid, clues):
    for side in xrange(len(grid)):
        for line in xrange(len(grid[side])):
            print check_line(grid, clues, side, line)


def find_impossible(grid, clues, side, line):
    pass


def method_overlap(grid, clues, side, line):
    """
    Simple overlap solving

    e.g. clue is 5 in a row of length 8:
    left as possible:  ooooo---
    right as possible: ---ooooo
    overlap:           ---oo---
    the middle two must be filled

    e.g.
    1 3 2 ----------
          --ooo----- # space for 1 and blank
          ----ooo--- # space for 2 and blank
          ----o----- # overlap
    """

    for c in xrange(len(clues[side][line])):
        # last cell in farthest possible left
        if c == 0:
            right_bound = clues[side][line][c] - 1
        else:
            right_bound = sum(clues[side][line][:c+1]) + c - 1
        # first cell in farthes possible right
        if c == len(grid[side][line]) - 1:
            left_bonud = len(grid[side][line]) - clues[side][line][c]
        else:
            left_bound = len(grid[side][line]) - (sum(clues[side][line][c:]) + (len(clues[side][line]) - c - 1))
        insert_range(grid, side, line, left_bound, right_bound)

def single_line_simplify(grid, clues, side, line):
    # clue = clues[side][line]
    method_overlap(grid, clues, side, line)

def sls_all(grid, clues):
    for side in xrange(len(grid)):
        for line in xrange(len(grid[side])):
            print_grid(grid)
            print side, line
            method_overlap(grid, clues, side, line)


def solve(clues):
    dim = map(len, clues)
    grid = [[[Mut(0) for _ in xrange(dim[1])] for _ in xrange(dim[0])]]
    grid.append([[grid[0][x][y] for x in xrange(dim[0])] for y in xrange(dim[1])])
    sls_all(grid, clues)
    print_grid(grid)


grid = [[0,1,0,1],
        [1,0,0,1],
        [1,1,0,0]]
clues = get_clues(grid)
print clues
solved = solve(clues)