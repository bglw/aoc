import unittest
import sys
from textwrap import dedent

rucksacks = open("data.txt", 'r').readlines()


def run(input):
    score = sum(map(scoreItem, map(findCommonItem, input)))
    return score


def findCommonItem(rucksack):
    size = len(rucksack)//2
    left, right = rucksack[:size], rucksack[size:]
    common = set(left).intersection(set(right))
    return common.pop()


def scoreItem(item):
    if item <= "z" and item >= "a":
        return ord(item) - 96
    else:
        return ord(item) - 38


class Adventest(unittest.TestCase):
    def test_run(self):
        data = dedent("""
            vJrwpWtwJgWrhcsFMMfFFhFp
            jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
            PmmdzqPrVvPwwTWBwg
            wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
            ttgJtRGJQctTZtZT
            CrZsJsPPZsGzwwsLwLmpwMDw
        """).lstrip().splitlines()
        self.assertEqual(run(data), 157)

    def test_common(self):
        common = findCommonItem("vJrwpWtwJgWrhcsFMMfFFhFp")
        self.assertEqual(common, "p")

    def test_score(self):
        self.assertEqual(scoreItem("a"), 1)
        self.assertEqual(scoreItem("A"), 27)
        self.assertEqual(scoreItem("Z"), 52)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(Adventest)
        unittest.TextTestRunner().run(suite)
    else:
        print(run(rucksacks))
