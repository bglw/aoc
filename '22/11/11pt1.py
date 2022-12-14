import re
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
    
    def round(self):
        if not len(self.items):
            return None, None
        item = self.items.pop(0)
        self.inspected += 1
        amt = self.amt if isinstance(self.amt, int) else item
        if self.op == "+":
            item += amt
        elif self.op == "*":
            item *= amt
        item //= 3
        if item % self.test == 0:
            return item, self.true_throw
        else:
            return item, self.false_throw

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def run(input: str):
    monkeys = [Monkey(m) for m in input.split("\n\n")]
    for _ in range(20):
        for m in monkeys:
            while len(m.items):
                item, next_monkey = m.round()
                if isinstance(item, int) and isinstance(next_monkey, int):
                    monkeys[next_monkey].items.append(item)
    monkey_business = [m.inspected for m in sorted(monkeys, key=lambda m: m.inspected)[-2:]]
    return monkey_business[0] * monkey_business[1]
    # return input


class Tests:

    def test_run(self):
        assert run(test_data) == test_data


test_data = """..."""


if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
