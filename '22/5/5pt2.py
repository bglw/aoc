import unittest
import sys
import re
from textwrap import dedent

crate_map = open("data.txt", 'r').read()


def run(input):
    crates, moves = split_board(input)
    stacks = parse_crates(crates)
    moves = map(parse_move, moves)
    for move in moves:
        make_moves(stacks, move)
    return ''.join(get_tops(stacks))


def split_board(input):
    crates, moves = input.split("\n\n")
    return crates, moves.splitlines()


def parse_move(move):
    directions = re.search(
        'move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)', move)
    return {
        "count": int(directions.group('count')),
        "from": int(directions.group('from')) - 1,
        "to": int(directions.group('to')) - 1
    }


def parse_crates(crates):
    lines = crates.splitlines()
    numbers = lines.pop()
    stacks = []
    for column in range(len(numbers)):
        if numbers[column].isdigit():
            stack = [line[column] for line in lines if column < len(line)]
            stack = list(filter(lambda char: char != " ", stack))
            stack.reverse()
            stacks.append(stack)
    return stacks


def make_moves(stacks, move):
    stacks[move["to"]].extend(stacks[move["from"]][-move["count"]:])
    del stacks[move["from"]][-move["count"]:]


def get_tops(stacks):
    return [stack[-1] for stack in stacks]


class Adventest(unittest.TestCase):
    def test_run(self):
        data = dedent("""
                [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3

            move 1 from 2 to 1
            move 3 from 1 to 3
            move 2 from 2 to 1
            move 1 from 1 to 2
        """)
        self.assertEqual(run(data), "MCD")

    def test_move_parse(self):
        directions = parse_move("move 1 from 2 to 1")
        self.assertEqual(directions, {
            "count": 1,
            "from": 1,
            "to": 0
        })

    def test_crates_parse(self):
        crates = dedent("""
                [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3
        """)
        stacks = parse_crates(crates)
        self.assertEqual(stacks, [
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        ])

    def test_multi_move(self):
        crates = dedent("""
                [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3
        """)
        directions = parse_move("move 2 from 2 to 1")
        stacks = parse_crates(crates)
        make_moves(stacks, directions)
        self.assertEqual(stacks, [
            ["Z", "N", "C", "D"],
            ["M"],
            ["P"],
        ])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(Adventest)
        unittest.TextTestRunner().run(suite)
    else:
        print(run(crate_map))
