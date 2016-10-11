# TODO: make get_clues dimension-ambiguous

class Mut:
    def __init__(self, val):
        self.val = val
    def get(self):
        return self.val
    def set(self, val):
        self.val = val


def get_clues(grid):
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
    print first, last
    for i in xrange(first, last+1):
        grid[side][line][i].set(1)


def method_overlap(grid, clues, side, line):
    """
    Simple overlap solving

    e.g. clue is 5 in a row of length 8:
    left as possible:  ooooo---
    right as possible: ---ooooo
    overlap:           ---oo---
    the middle two must be filled
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