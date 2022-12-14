import re
from collections import defaultdict
from tools import * 

test = False

def run(input: str):
    grid = [list(x) for x in input.splitlines()]
    width, height = len(grid[0]), len(grid)
    startX, startY = 0, 0
    for i, row in enumerate(grid):
        if "S" in row:
            startX = row.index("S")
            startY = i

    weights: list[list[None | int]] = [[None for _ in range(width)] for _ in range(height)]
    pts = [(startX, startY)]
    
    while len(pts):
        pt = pts.pop(0)
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pt = (pt[0] + dir[0], pt[1] + dir[1])
            current_weight = weights[pt[1]][pt[0]] or 0
            current_elv_char = grid[pt[1]][pt[0]]
            if current_elv_char == "S":
                current_elv_char = "a"
            current_elv = ord(current_elv_char) or 0
            if new_pt[0] < 0 or new_pt[0] >= width or new_pt[1] < 0 or new_pt[1] >= height:
                continue
            if weights[new_pt[1]][new_pt[0]] != None:
                continue

            new_elv_char = grid[new_pt[1]][new_pt[0]]
            at_goal = False
            if new_elv_char == "E":
                at_goal = True
                new_elv_char = "z"

            new_elv = ord(new_elv_char)
            if new_elv > current_elv + 1:
                continue

            if at_goal:
                return f"I can get there in {current_weight + 1} steps 🙂"

            weights[new_pt[1]][new_pt[0]] = current_weight + 1
            pts.append((new_pt[0], new_pt[1]))

    return None


class Tests:

    def test_run(self):
        global test
        test = True
        test_data = open("data_test.txt", 'r').read()
        run(test_data)

if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
