import re
from collections import defaultdict

X = 1
numb = 0
crt = [["." for _ in range(40)] for _ in range(6)]

def cycle(v):
    global numb, X, counts

    col = numb % 40
    row = numb // 40
    print(numb, row, col)

    if (X-1 <= (numb % 40) <= X+1):
        crt[row][col] = "#"

    numb += 1
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
    for row in crt:
        print(''.join(row))


class Tests:

    def test_run(self):
        assert run(test_data) == test_data


test_data = """noop
addx 3
addx -5"""


if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
