import re
from collections import defaultdict
import tools

test = False

def parseLine(input: str) -> list[int]:
    return tools.get_ints_with_neg(input)


def run(input: str):
    print("")
    lines = [parseLine(l) for l in input.splitlines()]
    target = 10 if test else 2000000
    reachable = set()
    for line in lines:
        sx, sy, bx, by  = line
        manhattan = abs(sx - bx) + abs(sy - by)
        if sy < target-manhattan or sy > target+manhattan:
            continue
        threshold = manhattan
        if sy > target:
            threshold = manhattan-(sy-target)
        if sy < target:
            threshold = manhattan-(target-sy)
        print(sy, "manhattan of", manhattan, "overlap of", threshold)
        sqs = threshold*2+1
        for x in range(sqs):
            reachable.add((sx - sqs//2) + x)

    for line in lines:
        sx, sy, bx, by  = line
        if by == target and bx in reachable:
            print("beacon in row, removing", bx)
            reachable.remove(bx)

    print(len(reachable))

    return "ok"


class Tests:

    def test_run(self):
        global test
        test = True
        test_data = open("data_test.txt", 'r').read()
        run(test_data)

if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
