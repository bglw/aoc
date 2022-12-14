import re
import decimal
import math
from collections import defaultdict

class Monkey:
    def __init__(self, input: str):
        attrs = (l.strip() for l in input.splitlines())
        next(attrs)
        self.items = [int(x) for x in next(attrs).removeprefix("Starting items: ").split(", ")]
        op, amt = next(attrs).removeprefix("Operation: new = old ").split()
        self.amt: int | str = amt
        self.op = op
        if amt != "old":
            self.amt = int(amt)
        self.test = int(next(attrs).removeprefix("Test: divisible by "))
        self.true_throw = int(next(attrs).removeprefix("If true: throw to monkey "))
        self.false_throw = int(next(attrs).removeprefix("If false: throw to monkey "))
        self.inspected = 0
    
    def round(self, lcm: int):
        if not len(self.items):
            return None, None
        item = self.items.pop(0)
        self.inspected += 1
        amt = self.amt if isinstance(self.amt, int) else item
        if self.op == "+":
            item += amt
        elif self.op == "*":
            item *= amt
        item %= lcm
        if item % self.test == 0:
            return item, self.true_throw
        else:
            return item, self.false_throw

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def run(input: str):
    monkeys = [Monkey(m) for m in input.split("\n\n")]
    lcm = math.lcm(*[m.test for m in monkeys])
    for r in range(10000):
        for m in monkeys:
            while len(m.items):
                item, next_monkey = m.round(lcm)
                if isinstance(item, int) and isinstance(next_monkey, int):
                    monkeys[next_monkey].items.append(item)
    monkey_business = [m.inspected for m in sorted(monkeys, key=lambda m: m.inspected)[-2:]]
    return monkey_business[0] * monkey_business[1]


class Tests:

    def test_run(self):
        assert run(test_data) == 2713310158


test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
