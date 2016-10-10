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

    for i in range(height):
        if row_clues[i][-1] < 0:
            row_clues[i][-1] = -row_clues[i][-1]
        row_clues[i] = row_clues[i][1:]
    for i in range(width):
        if col_clues[i][-1] < 0:
            col_clues[i][-1] = -col_clues[i][-1]
        col_clues[i] = col_clues[i][1:]
    return row_clues, col_clues
