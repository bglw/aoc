import re
import sys
from collections import defaultdict

test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read().replace("/", "//")
lines = input.splitlines()


def repl(monkey, num):
    global input
    if monkey == "root":
        print("Part 1:", num)
        quit()
    input = input.replace(monkey, str(num))


ans = None
while not ans:
    lines = input.splitlines()
    for i in reversed(range(len(lines))):
        if re.search(
                '^\d+', lines[i]):
            continue
        yell = re.search(
            '^(?P<monkey>\\w+): (?P<num>\\d+)$', lines[i])
        if yell:
            repl(yell.group("monkey"), yell.group("num"))
            continue
        math = re.search(
            '^(?P<monkey>\\w+): (?P<num>\\d+ .+ \\d+)$', lines[i])
        if math:
            repl(math.group("monkey"), eval(math.group("num")))
            continue
