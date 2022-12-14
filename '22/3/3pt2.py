import unittest
import sys
from textwrap import dedent

rucksacks = open("data.txt", 'r').readlines()


def run(input):
    elf_groups = chunker(input, 3)
    score = sum(map(scoreItem, map(findCommonItem, elf_groups)))
    return score


def findCommonItem(rucksacks):
    common = set(rucksacks[0].strip()).intersection(
        set(rucksacks[1].strip())).intersection(set(rucksacks[2].strip()))
    return common.pop()


def scoreItem(item):
    if item <= "z" and item >= "a":
        return ord(item) - 96
    else:
        return ord(item) - 38


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


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
        self.assertEqual(run(data), 70)

    def test_common(self):
        common = findCommonItem([
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg"
        ])
        self.assertEqual(common, "r")

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
