import re
from collections import defaultdict

X = 1
numb = 0
counts = []

def cycle(v):
    global numb, X, counts
    numb += 1

    if numb == 20 or (numb > 20 and (numb - 20) % 40 == 0):
        counts.append(X * numb)

    X += v

def run(input: str):
    instructions = input.splitlines()
    for ins in instructions:
        if ins == "noop":
            cycle(0)
        else:
            v = int(ins.split()[1])
            cycle(0)
            cycle(v)
    return sum(counts)

class Tests:

    def test_run(self):
        assert run(test_data) == test_data


test_data = """noop
addx 3
addx -5"""


if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
