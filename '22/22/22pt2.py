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
world = set()
start = None
for y, line in enumerate(lines):
    for x, char in enumerate(list(line)):
        if char == ".":
            tiles.add((x+1, y+1))
            world.add((x+1, y+1))
            if not start:
                start = (x+1, y+1)
        if char == "#":
            walls.add((x+1, y+1))
            world.add((x+1, y+1))

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

warps = {}
edge = range(1, 51)
# A
for p in edge:
    warps[(p+50, 0)] = ((1, p+150), 1)
    warps[(0, p+150)] = ((p+50, 1), -1)
# B
for p in edge:
    warps[(p+100, 0)] = ((p, 200), 0)
    warps[(p, 201)] = ((p+100, 1), 0)
# C
for p in edge:
    warps[(151, p)] = ((100, 151-p), 2)
    warps[(101, 151-p)] = ((150, p), -2)
# D
for p in edge:
    warps[(p+100, 51)] = ((100, p+50), 1)
    warps[(101, p+50)] = ((p+100, 50), -1)
# E
for p in edge:
    warps[(p+50, 151)] = ((50, p+150), 1)
    warps[(51, p+150)] = ((p+50, 150), -1)
# F
for p in edge:
    warps[(50, p)] = ((1, 151-p), 2)
    warps[(0, 151-p)] = ((51, p), -2)
# G
for p in edge:
    warps[(50, p+50)] = ((p, 101), -1)
    warps[(p, 100)] = ((51, p+50), 1)


def rotate(dir, clockwise):
    match dir:
        case (1, 0):
            return (0, 1 if clockwise else -1)
        case (-1, 0):
            return (0, -1 if clockwise else 1)
        case (0, 1):
            return (-1 if clockwise else 1, 0)
        case (0, -1):
            return (1 if clockwise else -1, 0)


def rotate_movement(dir, amt):
    abs_amt = abs(amt)
    clockwise = amt > 0
    for _ in range(abs_amt):
        dir = rotate(dir, clockwise)
    return dir


pos = start
lastmove = (0, 0)
while len(moves):
    count, move = moves.pop(0)
    print("Moving ", count, "times in the direction", move)
    lastmove = move
    for done in range(count):
        nextpos = (pos[0] + move[0], pos[1] + move[1])
        if nextpos in tiles:
            print("Now at", nextpos)
            pos = nextpos
            continue
        elif nextpos in walls:
            print("Wall at", nextpos, "stopping at", pos)
            break
        else:
            next, rotation = warps[nextpos]
            remaining = count - done - 1
            print("Void at", nextpos, "Warping to", next,
                  "with", remaining, "moves remaining")
            if next in walls:
                print("Was a wall, nevermind")
                break
            pos = next
            moves.insert(0, (remaining, move))
            for i in range(len(moves)):
                c, m = moves[i]
                moves[i] = (c, rotate_movement(m, rotation))
            print("Now moving", moves[i])
            break

facing = 0
if lastmove[0] == -1:
    facing = 2
if lastmove[1] == -1:
    facing = 3
if lastmove[1] == 1:
    facing = 1


print((1000 * (pos[1])) + (4 * (pos[0])) + facing)
print("Concluded at", pos[0], pos[1])
