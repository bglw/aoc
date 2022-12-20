import re
import sys
from collections import defaultdict
import tools

test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()

nums = [int(x) for x in lines]
mult_nums = [int(x)*811589153 for x in lines]

positions = [x for x in range(len(nums))]
for i in range(len(nums)):
    index = positions.index(i)
    next = index + nums[i]
    item = positions.pop(index)
    next %= len(positions)
    positions.insert(next, item)

list = [nums[i] for i in positions]
zero = list.index(0)
print("Part 1:", list[(zero + 1000) % len(list)]+list[(zero + 2000) %
      len(list)]+list[(zero + 3000) % len(list)])

positions = [x for x in range(len(mult_nums))]
for _ in range(10):
    for i in range(len(mult_nums)):
        index = positions.index(i)
        next = index + mult_nums[i]
        item = positions.pop(index)
        next %= len(positions)
        positions.insert(next, item)

list = [mult_nums[i] for i in positions]
zero = list.index(0)
print("Part 2:", list[(zero + 1000) % len(list)]+list[(zero + 2000) %
      len(list)]+list[(zero + 3000) % len(list)])
