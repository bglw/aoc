import unittest
import sys
from textwrap import dedent

played = ["A", "B", "C"]
response = ["X", "Y", "Z"]

strategy = open("data.txt", 'r').readlines()


def run(input):
    score = 0
    for move in input:
        score += conductTurn(*(move.strip().split(' ')))
    return score


def conductTurn(them, me):
    them = played.index(them)

    if me == "X":
        return scoreTurn(them, them - 1)
    if me == "Y":
        return scoreTurn(them, them)
    if me == "Z":
        return scoreTurn(them, (them + 1) % 3)


def scoreTurn(them, me):
    if me < 0:
        me = 2
    score = me + 1
    if them == (me + 1) % 3:
        return score + 0
    if them == me:
        return score + 3
    return score + 6


class Adventest(unittest.TestCase):
    def test_run(self):
        data = dedent("""
            A Y
            B X
            C Z
        """).lstrip().splitlines()
        self.assertEqual(run(data), 12)

    def test_score_turn(self):
        self.assertEqual(conductTurn("A", "Y"), 4)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(Adventest)
        unittest.TextTestRunner().run(suite)
    else:
        print(run(strategy))
