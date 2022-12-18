import re
from collections import defaultdict
import tools

test = False

# Used to make the output file prettier, not part of the aoc submission itself
def trimmed_grid(grid):
    highest = 0
    for i,row in enumerate(grid):
        if row.count('o'):
            highest = i
    
    grid = tools.transpose(grid[:highest+2])

    lowest = -1
    for i,col in enumerate(grid):
        if col.count('o'):
            if lowest == -1:
                lowest = i
            highest = i

    return tools.transpose(grid[lowest-2:highest+2])

# Get all points in a line
def pts(pfrom, pto) -> list[list[int]]:
    if pfrom[0] == pto[0]:
        return [[pfrom[0], x] for x in range(pto[1],pfrom[1],1 if pto[1]<pfrom[1] else -1)] + [pfrom]
    else:
        return [[x, pfrom[1]] for x in range(pto[0],pfrom[0],1 if pto[0]<pfrom[0] else -1)] + [pfrom]

def move_sand(grid):
    dirs = [(1, 0), (1, -1), (1, 1)]
    pr,pc = 0, 500
    state = "FALLING"
    while state == "FALLING":
        for dir in dirs:
            r,c = pr+dir[0],pc+dir[1]
            if len(grid) == r or len(grid[pc]) == c or c < 0:
                grid[pr][pc] = " "
                return "ABYSS"
            if grid[r][c] == " ":
                grid[pr][pc] = " "
                grid[r][c] = "O"
                pr, pc = r, c
                break
        else:
            grid[pr][pc] = "o"
            return "REST"

def run(input: str):
    print("")
    # Making an arbitrarily large grid in lieu of making one that can resize
    grid = [[" " for _ in range(1000)] for _ in range(1000)]
    rock_paths = [[[int(g) for g in v.split(',')] for v in l.split(' -> ')] for l in input.splitlines()]
    for path in rock_paths:
        for i, point in enumerate(path):
            if i == len(path) - 1:
                break
            pfrom, pto = point, path[i+1]
            for c,r in pts(pfrom, pto):
                grid[r][c] = '#'

    at_rest = 0
    while move_sand(grid) != "ABYSS":
        at_rest += 1

    print(at_rest)

    grid[0][500] = "+"
    f = open("out-p1.txt", "w")
    f.write('\n'.join([''.join(subgrid) for subgrid in trimmed_grid(grid)]))
    f.close()
    return ""


class Tests:

    def test_run(self):
        global test
        test = True
        test_data = open("data_test.txt", 'r').read()
        run(test_data)

if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
