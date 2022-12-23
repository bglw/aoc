import re
import sys
from collections import defaultdict

test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()

map = set()

for row, line in enumerate(lines):
    for col, sq in enumerate(list(line)):
        if sq == "#":
            map.add((col, row))

cardinal_dirs = [(-1, -1), (0, -1), (1, -1), (1, 0),
                 (-1, 0), (-1, 1), (0, 1), (1, 1)]

order_of_choices = [
    ((0, 1, 2), (0, -1)),
    ((5, 6, 7), (0, 1)),
    ((0, 4, 5), (-1, 0)),
    ((2, 3, 7), (1, 0)),
]

rounds = 0
map_at_round_ten = None
while True:
    moves = {}
    elves = list(map)
    sqs, forbidden = set(), set()
    for i, elf in enumerate(elves):
        neighbors = {}
        for id, dir in enumerate(cardinal_dirs):
            sq = (elf[0] + dir[0], elf[1] + dir[1])
            if sq in map:
                neighbors[id] = True
        if not neighbors:
            continue
        for check_dirs, move_to in order_of_choices:
            if check_dirs[0] not in neighbors and check_dirs[1] not in neighbors and check_dirs[2] not in neighbors:
                moves[i] = (elf[0] + move_to[0], elf[1] + move_to[1])
                break
        if i not in moves:
            continue
        if moves[i] in sqs:
            # An elf wants to move here already, neither of us should move
            forbidden.add(moves[i])
        else:
            sqs.add(moves[i])

    moved = 0
    for elf, move in moves.items():
        if move not in forbidden:
            map.remove(elves[elf])
            elves[elf] = move
            map.add(elves[elf])
            moved += 1

    rounds += 1
    if rounds == 10:
        map_at_round_ten = map.copy()
    if not moved:
        break
    order_of_choices.append(order_of_choices.pop(0))

min_col = min(*[e[0] for e in map_at_round_ten])
max_col = max(*[e[0] for e in map_at_round_ten])
min_row = min(*[e[1] for e in map_at_round_ten])
max_row = max(*[e[1] for e in map_at_round_ten])

empty_tiles = 0
for r in range(min_row, max_row+1):
    line = []
    for c in range(min_col, max_col+1):
        line.append("#" if (c, r) in map_at_round_ten else ".")
        if (c, r) not in map_at_round_ten:
            empty_tiles += 1
    if test:
        print(''.join(line))

print("Part 1:", empty_tiles)
print("Part 2:", rounds)
