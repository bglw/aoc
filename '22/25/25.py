import re
import sys
from collections import defaultdict

test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()


def char2num(c):
    if c.isnumeric():
        return int(c)
    elif c == "-":
        return -1
    elif c == "=":
        return -2


def num2char(n):
    if n == -2:
        return "="
    if n == -1:
        return "-"
    if n >= 0 and n <= 2:
        return str(n)
    assert False


def s2d(s):
    num = 0
    for i, char in enumerate(reversed(list(s))):
        num += (5**i) * char2num(char)
    return num


def d2s(s):
    num = ['2']
    max_exp = 0
    while s2d(num) < s:
        max_exp += 1
        num.append('2')

    diff = s2d(num) - s
    while diff != 0:
        for i, v in enumerate(num):
            exp = len(num)-i-1
            if diff >= (5**exp):
                num[i] = num2char(char2num(v) - 1)
                break
        nextdiff = s2d(num) - s
        assert nextdiff != diff
        diff = nextdiff

    return ''.join(num)


sum = 0
for line in lines:
    sum += s2d(line)

print(d2s(sum))
