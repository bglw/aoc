import re
from collections import defaultdict


def run(input: str):
    orig = input.splitlines()
    w = len(orig[0])
    h = len(orig)

    map = []
    for row in range(h):
        map.append(["`"] * w)

    for row in range(h):
        trees = count_visible(orig[row])
        for tree in trees:
            map[row][tree] = "•"
        trees = count_visible(orig[row][::-1])
        for tree in trees:
            map[row][-tree-1] = "•"

    for column in range(w):
        col = ""
        for row in range(h):
            col = col + orig[row][column]
        trees = count_visible(col)
        for tree in trees:
            map[tree][column] = "•"
        trees = count_visible(col[::-1])
        for tree in trees:
            map[-tree-1][column] = "•"

    assembled = []
    for row in range(h):
        assembled.append(''.join(map[row]))

    all = '\n'.join(assembled)
    return all.count('•')


def count_visible(row):
    cap, trees = -1, []
    for i in range(len(row)):
        tree = int(row[i])
        if tree > cap:
            trees.append(i)
            cap = tree
    return trees


class Tests:

    def test_count_visible(self):
        assert count_visible("30375") == [0, 3]
        assert count_visible("30375"[::-1]) == [0, 1]
        assert count_visible("1234") == [0, 1, 2, 3]

    def test_run(self):
        assert run(test_data) == 21

    def test_another_run(self):
        assert run(hand_test_data) == 14


test_data = """30373
25512
65332
33549
35390"""

hand_test_data = """30703
11111
77777"""


if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
