import unittest
import sys
import re
from textwrap import dedent

stream = open("data.txt", 'r').read()


def run(input):
    for index in range(len(input[3:])):
        if (len(set(input[index:index+4])) == 4):
            return index + 4


class Adventest(unittest.TestCase):
    def test_run(self):
        data = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
        self.assertEqual(run(data), 7)

    def test_another_run(self):
        data = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
        self.assertEqual(run(data), 10)

    def test_yet_another_run(self):
        data = "nppdvjthqldpwncqszvftbrmjlhg"
        self.assertEqual(run(data), 6)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(Adventest)
        unittest.TextTestRunner().run(suite)
    else:
        print(run(stream))
