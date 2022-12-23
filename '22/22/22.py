import re
import sys
from collections import defaultdict

test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
board, instructions = input.split("\n\n")
lines = board.splitlines()

tiles = set()
walls = set()
start = None
for y, line in enumerate(lines):
    for x, char in enumerate(list(line)):
        if char == ".":
            tiles.add((x, y))
            if not start:
                start = (x, y)
        if char == "#":
            walls.add((x, y))

instructions = re.sub(r'(R|L)', r',\1,', instructions)
moves = []
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
dir = 0
for instruction in instructions.split(','):
    if instruction == "R":
        dir = (dir + 1) % len(dirs)
    elif instruction == "L":
        dir = (dir - 1) % len(dirs)
    else:
        moves.append((int(instruction), dirs[dir]))

pos = start
lastmove = (0, 0)
while len(moves):
    count, move = moves.pop(0)
    lastmove = move
    for _ in range(count):
        nextpos = (pos[0] + move[0], pos[1] + move[1])
        print(pos, nextpos)
        if nextpos in tiles:
            print(pos)
            pos = nextpos
            continue
        elif nextpos in walls:
            print("ACK")
            break
        else:
            wrapped = pos
            for _ in range(10000):
                t = (wrapped[0] - move[0], wrapped[1] - move[1])
                if t in tiles or t in walls:
                    wrapped = t
                else:
                    break
            if wrapped in walls:
                break
            else:
                print(pos)
                pos = wrapped

print(pos[0]+1, pos[1]+1)
print(lastmove)
facing = 0
if lastmove[0] == -1:
    facing = 2
if lastmove[1] == -1:
    facing = 3
if lastmove[1] == 1:
    facing = 1

print((1000 * (pos[1]+1)) + (4 * (pos[0]+1)) + facing)
