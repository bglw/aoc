import re
import sys
from collections import defaultdict
import heapq

test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()
grid = [list(r.replace(">", ".").replace("<", ".").replace(
    "^", ".").replace("v", ".")) for r in lines]

walls = set()
minute_zero_blizzards = []
row_goal = len(lines) - 1
col_goal = len(lines[0]) - 2
for row, line in enumerate(lines):
    for col, char in enumerate(list(line)):
        if char == "#":
            walls.add((col, row))
        if char == '>':
            minute_zero_blizzards.append(((col, row), (1, 0)))
        if char == '<':
            minute_zero_blizzards.append(((col, row), (-1, 0)))
        if char == 'v':
            minute_zero_blizzards.append(((col, row), (0, 1)))
        if char == '^':
            minute_zero_blizzards.append(((col, row), (0, -1)))


def get_blizzard_set(b):
    # Get all blizzards at a given minute as a set for easy comparison
    return {x[0] for x in b}


blizzard_timeslices = [
    (minute_zero_blizzards, get_blizzard_set(minute_zero_blizzards))]
dirs = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def calc_next_blizzard():
    # Add a new memoized blizzard state for the next unfilled timeslot
    appending = []
    building_upon, _ = blizzard_timeslices[-1]
    for b, (blizzard_pos, blizzard_dir) in enumerate(building_upon):
        next_pos = (blizzard_pos[0] + blizzard_dir[0],
                    blizzard_pos[1] + blizzard_dir[1])
        if next_pos in walls:
            prev_pos = blizzard_pos
            eval_pos = blizzard_pos
            while True:
                eval_pos = (prev_pos[0] - blizzard_dir[0],
                            prev_pos[1] - blizzard_dir[1])
                if eval_pos not in walls:
                    prev_pos = eval_pos
                else:
                    break
            appending.append((prev_pos, blizzard_dir))
        else:
            appending.append((next_pos, blizzard_dir))
    blizzard_timeslices.append((appending, get_blizzard_set(appending)))


def get_blizzard(time):
    while len(blizzard_timeslices) < time+1:
        calc_next_blizzard()
    return blizzard_timeslices[time][1]


def run(start_time, start_square, target_square):

    def heur(pos, time):
        # A* heuristic of manhattan distance + time elapsed
        return ((target_square[0] - pos[0]) + (target_square[1] - pos[1])) + time

    q = [(heur(start_square, start_time),
          (start_square, [start_square], start_time))]

    best_chain, best_time = None, None
    seen = set()
    while len(q):
        _, (pos, chain, time) = heapq.heappop(q)
        if (pos, time) in seen:
            continue
        seen.add((pos, time))
        if pos == target_square:
            best_chain = chain
            best_time = time - start_time
            q.clear()
            continue
        next_time = time + 1
        next_blizzard = get_blizzard(next_time)
        for dir in dirs:
            next_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] > col_goal or next_pos[1] > row_goal:
                continue
            if next_pos in walls or next_pos in next_blizzard:
                continue
            next_chain = None
            if test:
                next_chain = chain.copy()
                next_chain.append(next_pos)
            heapq.heappush(
                q, (heur(next_pos, next_time), (next_pos, next_chain, next_time)))

    if test and start_time == 0:
        for i, pos in enumerate(best_chain):
            print("\nMinute", i)

            i_grid = [r.copy() for r in grid]
            i_grid[pos[1]][pos[0]] = 'E'

            i_blizz, _ = blizzard_timeslices[i]
            for blizz in i_blizz:
                exst = i_grid[blizz[0][1]][blizz[0][0]]
                if exst == ">" or exst == "<" or exst == "^" or exst == "v":
                    i_grid[blizz[0][1]][blizz[0][0]] = 2
                elif exst != ".":
                    i_grid[blizz[0][1]][blizz[0][0]
                                        ] = i_grid[blizz[0][1]][blizz[0][0]] + 1
                else:
                    if blizz[1] == (1, 0):
                        i_grid[blizz[0][1]][blizz[0][0]] = ">"
                    if blizz[1] == (-1, 0):
                        i_grid[blizz[0][1]][blizz[0][0]] = "<"
                    if blizz[1] == (0, 1):
                        i_grid[blizz[0][1]][blizz[0][0]] = "v"
                    if blizz[1] == (0, -1):
                        i_grid[blizz[0][1]][blizz[0][0]] = "^"

            print('\n'.join([''.join([str(c) for c in r]) for r in i_grid]))

        print("---\nDone printing part 1 round 1 viz\n---")

    return best_time


t1 = run(0, (1, 0), (col_goal, row_goal))
t2 = run(t1, (col_goal, row_goal), (1, 0))
t3 = run(t1+t2, (1, 0), (col_goal, row_goal))

print("Part 1:", t1)
print("Part 2:", sum([t1, t2, t3]))
