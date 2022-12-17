import os
import itertools

for part in [1, 2]:
    test = 'AOC_TEST' in os.environ
    file = "data_test.txt" if test else "data.txt"
    input = open(file, 'r').read()

    dirs = itertools.cycle([(i, (1, 0)) if d == ">" else (i, (-1, 0))
                            for i, d in enumerate(list(input))])
    rocks = itertools.cycle([
        (0, [(0, 0), (1, 0), (2, 0), (3, 0)]),
        (1, [(1, 0), (1, -1), (0, -1), (2, -1), (1, -2)]),
        (2, [(0, 0), (1, 0), (2, 0), (2, -1), (2, -2)]),
        (3, [(0, 0), (0, -1), (0, -2), (0, -3)]),
        (4, [(0, 0), (1, 0), (0, -1), (1, -1)]),
    ])

    width = 7
    fallen = 0
    settled = set([(i, 1) for i in range(7)])
    edges = set([tuple([0 for _ in range(7)])])
    top = tuple([1 for _ in range(7)])

    def get_height():
        return abs(min(list([x-1 for x in top])))

    def update_state(rock):
        global top
        for pt in rock:
            settled.add(pt)
        next_top = list(top)
        for x, y in rock:
            next_top[x] = min(top[x], y)
        top = tuple(next_top)

    def init_rock(rock):
        return [(x+2, y+min(top)-4) for x, y in rock]

    def move_rock(rock, dir):
        next_rock = [(x+dir[0], y+dir[1]) for x, y in rock]
        for pt in next_rock:
            if pt[0] >= width or pt[0] < 0:
                return rock, False
            if pt in settled:
                return rock, True
        return next_rock, False

    end_goal = 2022 if part == 1 else 1000000000000

    previous_pattern = (0, 0)
    steps_since_previous_pattern = []

    while fallen < end_goal:
        fallen += 1
        rock_id, rock = next(rocks)
        rock, at_rest = init_rock(rock), False

        dir_id = 0
        while not at_rest:
            dir_id, dir = next(dirs)
            rock, _ = move_rock(rock, dir)
            rock, at_rest = move_rock(rock, [0, 1])

        update_state(rock)

        if (previous_pattern[0]):
            steps_since_previous_pattern.append(
                get_height() - previous_pattern[0])

        pattern_baseline = max(top)
        pattern = tuple([x - pattern_baseline for x in top]) + \
            (rock_id, dir_id)

        if pattern in edges:
            new_height = get_height()
            if (previous_pattern[0]):
                pattern_blocks = fallen - previous_pattern[1]
                pattern_height = new_height - previous_pattern[0]
                remaining_cycles = (end_goal - fallen) // pattern_blocks

                future_height = remaining_cycles * pattern_height + new_height
                partial_remaining_cycle = end_goal - \
                    (fallen + remaining_cycles * pattern_blocks)
                top = tuple(
                    [future_height + steps_since_previous_pattern[partial_remaining_cycle-1]+1])

                fallen = end_goal
            else:
                edges = set()
                previous_pattern = (get_height(), fallen)

        edges.add(pattern)

    print(f"Part {part}:", abs(min(list([x-1 for x in top]))))
