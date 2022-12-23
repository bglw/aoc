import re
import sys
from collections import defaultdict

# This file represents my attempt to actually solve this problem for any cube,
# but the logic has bested me and 22pt2.py contains the hardcoded version.

# The intention was to determine the required logic for following edges around the circumference
# and determining where that point would re-enter the cube.
# It can resolve simple and semi-complex moves between edges, but doesn't yet handle
# keeping track of the edges to navigate halfway around the circumference.

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


def neighbors_of(pt, horiz, dist):
    if horiz:
        return [(pt[0]+dist, pt[1]), (pt[0]-dist, pt[1])]
    else:
        return [(pt[0], pt[1]+dist), (pt[0], pt[1]-dist)]


def determine_edge(inner, outer, horiz):
    edge_length = 1
    resolved = None
    len1, len2 = 0, 0
    while not resolved:
        out1, out2 = neighbors_of(outer, horiz, edge_length)
        in1, in2 = neighbors_of(inner, horiz, edge_length)

        if out1 in world:
            edge_outer, _ = neighbors_of(outer, horiz, edge_length - 1)
            resolved = ("CORNER", out1, edge_outer)
            break
        if out2 in world:
            _, edge_outer = neighbors_of(outer, horiz, edge_length - 1)
            resolved = ("CORNER", out2, edge_outer)
            break

        if in1 in world:
            len1 += 1
        if in2 in world:
            len2 += 1

        if in1 not in world and in2 not in world:
            shorter_toward_1 = len1 < len2
            closest1, closest2 = neighbors_of(
                inner, horiz, min(len1, len2))
            closest1_outer, closest2_outer = neighbors_of(
                inner, horiz, min(len1, len2)+1)
            edge_length = min(len1, len2)+1
            resolved = (
                "EDGE",
                closest1 if shorter_toward_1 else closest2,
                closest1_outer if shorter_toward_1 else closest2_outer
            )
            break

        edge_length += 1
    return {
        "type": resolved[0],
        "next_pt_inner": resolved[1],
        "next_pt_outer": resolved[2],
        "distance": edge_length-1
    }


def move_along_edge(inner, outer, dist, turns=1):
    horiz = inner[0] == outer[0]
    print("Moving along", inner, outer, "a distance of", dist)
    pt = None
    clockwise = True
    edge_length = 1
    while not pt:
        out1, out2 = neighbors_of(outer, horiz, edge_length)
        in1, in2 = neighbors_of(inner, horiz, edge_length)
        if {out1, out2} & world:
            lastpt = pt
            clockwise = out1 in world
            for d in range(dist):
                p1, p2 = neighbors_of(inner, horiz, d)
                op1, op2 = neighbors_of(outer, horiz, d)
                pt = (p2, op2) if clockwise else (p1, op1)
                if pt[0] not in world:
                    print("Reached", pt[0], "which is no longer on the edge")
                    return move_along_edge(lastpt[0], pt[0], dist - d - 1, turns + 1)
                lastpt = pt
        elif not ({in1, in2} & world):
            lastpt = pt
            clockwise = in1 not in world
            for d in range(dist):
                p1, p2 = neighbors_of(inner, horiz, d)
                op1, op2 = neighbors_of(outer, horiz, d)
                pt = (p2, op2) if clockwise else (p1, op1)
                if pt[0] not in world:
                    print("Reached", pt[0], "which is no longer on the edge")
                    return move_along_edge(lastpt[0], pt[0], dist - d - 1, turns + 1)
                lastpt = pt
        elif edge_length == dist:
            in1, in2 = neighbors_of(inner, horiz, dist)
            out1, out2 = neighbors_of(outer, horiz, dist)
            clockwise = in1 not in world
            pt = (in2, out2) if clockwise else (in1, out1)
    if pt[0] not in world:
        print("BAD PT", pt)
        quit()
    return (pt, turns, clockwise)


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
            print("Found the void at", nextpos)
            outer = nextpos
            search_horiz = move[0] == 0
            result = determine_edge(pos, outer, search_horiz)
            print("Resolved as", result)
            if result["type"] == "CORNER":
                point, turns, clockwise = move_along_edge(
                    result["next_pt_inner"],
                    result["next_pt_outer"],
                    result["distance"]
                )
                print("Warped to", point[0])
                pos = point[0]
                remaining_steps = count - done - 1
                moves.insert(0, (remaining_steps, move))
                for i in range(len(moves)):
                    c, move = moves[i]
                    moves[i] = (c, rotate_movement(
                        move, turns if clockwise else -turns))
                break
            else:
                skip_edge = determine_edge(
                    result["next_pt_inner"], result["next_pt_outer"], not search_horiz)
                assert skip_edge["type"] == "CORNER"
                point, turns, clockwise = move_along_edge(
                    skip_edge["next_pt_inner"],
                    skip_edge["next_pt_outer"],
                    skip_edge["distance"]+1
                )
                print("Evaluating from point", point)
                quit()


facing = 0
if lastmove[0] == -1:
    facing = 2
if lastmove[1] == -1:
    facing = 3
if lastmove[1] == 1:
    facing = 1


print((1000 * (pos[1])) + (4 * (pos[0])) + facing)
print("Concluded at", pos[0], pos[1])
