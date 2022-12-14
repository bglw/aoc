import re
from collections import defaultdict


def run(input):
    rows = input.splitlines()
    w = len(rows[0])
    h = len(rows)
    max = 0
    for x in range(w):
        for y in range(h):
            t = eval_tree(input, x, y)
            if (t > max):
                max = t
    return max


def eval_tree(input: str, c: int, r: int):
    rows = input.splitlines()
    treerow = rows[r]
    tree = treerow[c]
    left = treerow[0:c][::-1]
    right = treerow[c+1:]
    cols = list(map(lambda i: ''.join(
        map(lambda row: row[i], rows)), range(len(rows[0]))))
    treecol = cols[c]
    up = treecol[0:r][::-1]
    down = treecol[r+1:]

    return len(count_visible(left, int(tree))) * len(count_visible(right, int(tree))) * \
        len(count_visible(up, int(tree))) * \
        len(count_visible(down, int(tree)))


def count_visible(row, init=-1):
    cap, trees = init, []
    for i in range(len(row)):
        tree = int(row[i])
        if tree < cap:
            trees.append(i)
        else:
            trees.append(i)
            return trees
    return trees


class Tests:

    def test_cv(self):
        assert len(count_visible("45678", 6)) == 3

    def test_eval_tree(self):
        assert eval_tree(test_data, 2, 3) == 8

    def test_eval_tree2(self):
        assert eval_tree(test_data, 2, 1) == 4
        assert eval_tree(test_data, 2, 0) == 0
        assert eval_tree(test_data, 4, 2) == 0
        assert eval_tree(test_data, 1, 1) == 1
        assert eval_tree(test_data, 2, 2) == 1
        assert eval_tree(hand_test_data, 1, 1) == 2

    def test_run(self):
        assert run(test_data) == 8


test_data = """30373
25512
65332
33549
35390"""

hand_test_data = """30703
11011
77777"""


if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
