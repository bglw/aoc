import unittest
import sys
from textwrap import dedent

cleaning_areas = open("data.txt", 'r').readlines()


def run(input):
    return len(filter(pair_contains, input))


def pair_contains(pair):
    a, b = pair.split(",")
    return a_in_b(a, b) or a_in_b(b, a) or False


def a_in_b(a, b):
    a, b = split(a), split(b)
    return (b[0] <= a[0] <= b[1]) or (b[0] <= a[1] <= b[1])


def split(range):
    return map(int, range.split("-"))


class Adventest(unittest.TestCase):
    def test_run(self):
        data = dedent("""
            2-4,6-8
            2-3,4-5
            5-7,7-9
            2-8,3-7
            6-6,4-6
            2-6,4-8
        """).lstrip().splitlines()
        self.assertEqual(run(data), 4)

    def test_contain(self):
        contains = a_in_b("3-7", "2-8")
        self.assertTrue(contains)
        contains = a_in_b("3-9", "2-8")
        self.assertTrue(contains)
        contains = a_in_b("1-2", "3-4")
        self.assertFalse(contains)

    def test_pair(self):
        contains = pair_contains("3-7,2-8")
        self.assertTrue(contains)
        contains = pair_contains("2-8,3-8")
        self.assertTrue(contains)
        contains = pair_contains("2-8,3-9")
        self.assertTrue(contains)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(Adventest)
        unittest.TextTestRunner().run(suite)
    else:
        print(run(cleaning_areas))
