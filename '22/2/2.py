import unittest
import sys
from textwrap import dedent

played = ["A", "B", "C"]
response = ["X", "Y", "Z"]

strategy = open("data.txt", 'r').readlines()


def run(input):
    score = 0
    for move in input:
        score += scoreTurn(*(move.strip().split(' ')))
    return score


def scoreTurn(them, me):
    them = played.index(them)
    me = response.index(me)
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
        self.assertEqual(run(data), 15)

    def test_score_turn(self):
        self.assertEqual(scoreTurn("A", "Y"), 2 + 6)
        self.assertEqual(scoreTurn("A", "Z"), 3 + 0)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(Adventest)
        unittest.TextTestRunner().run(suite)
    else:
        print(run(strategy))
