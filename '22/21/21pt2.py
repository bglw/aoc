import re
import sys
from collections import defaultdict
from z3 import *


test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read().replace("/", "/")
input = re.sub(r'(root: \w+ ).( \w+)', r'\1, root == \2', input)
input = re.sub(r'humn: \d+', r'humn: x', input)

rawmonkeys = {line.split(':')[0]: line for line in input.splitlines()}
monkeys = {line.split(':')[0]: Real(line.split(':')[0])
           for line in input.splitlines()}

input = re.sub(r'(\w+):', r'\1 ==', input)
lines = [re.sub(r'(\w{4})', r'monkeys["\1"]', line)
         for line in input.splitlines()]

s = Solver()
x = Real('x')
eval(f"s.add(And(*[{', '.join(lines)}]))")
r = s.check()
for id in ["root", "zzfw"]:
    print(rawmonkeys[id], "-->", s.model()[monkeys[id]])
print("Part 2: ", s.model()[x])
