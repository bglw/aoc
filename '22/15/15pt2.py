import re
from collections import defaultdict
import tools

test = False

def parseLine(input: str) -> list[int]:
    sx, sy, bx, by  = tools.get_ints_with_neg(input)
    return [sx, sy, abs(sx - bx) + abs(sy - by)]

def run(input: str):
    print("")
    lines = [parseLine(l) for l in input.splitlines()]

    max = 20 if test else 4000000

    for report in lines:
        sx, sy, manhattan = report
        r = manhattan+1
        for p in range(r):
            for p in [(sx - p, sy - (r - p))
                        , (sx + p, sy - (r - p))
                        , (sx - p, sy + (r - p))
                        , (sx + p, sy + (r - p))]:
                if p[0] < 0 or p[0] > max or p[1] < 0 or p[1] > max:
                    continue
                within = 0
                for innerReport in lines:
                    isx, isy, imanhattan = innerReport
                    dist = abs(p[0] - isx) + abs(p[1] - isy)
                    if (dist <= imanhattan):
                        within += 1
                        break

                if not within:
                    print("FOUND", p)
                    print(p[0] * 4000000 + p[1])
                    quit()

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
