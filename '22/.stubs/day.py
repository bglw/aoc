import re
import os
from collections import defaultdict
import tools

test = 'AOC_TEST' in os.environ
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()

print(input)
