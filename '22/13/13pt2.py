import re
from collections import defaultdict
from tools import * 
import itertools
import functools

test = False

class Packet:
    def __init__(self, input: str):
        self.raw = input
        self.input = list(input)
        self.values = []
        self.building_lists = []
        while len(self.input):
            self.read()
        assert len(self.building_lists) == 0

    def append_raw(self, raw):
        if len(self.building_lists):
            self.building_lists[-1].append(raw)
        else:
            self.values.append(raw)

    # I realised after writing all of this that I could have simply piped
    # each line through eval() :liam-facepalm:

    def read(self):
        c = self.input.pop(0)
        if c.isdigit():
            # Grab all of the subsequent digits (for long numbers)
            while len(self.input) and self.input[0].isdigit():
                c += self.input.pop(0)

            self.append_raw(int(c))
            c = self.input.pop(0)

        if c == ']':
            self.append_raw(self.building_lists.pop())
        elif c == '[':
            self.building_lists.append(list())
        elif c == ",":
            pass
        else:
            assert False

    def compare_with(self, right) -> int:
        for left, right in  itertools.zip_longest(self.values, right.values):
            verdict = pair_ordered(left, right)
            if verdict == True:
                return -1
                break
            elif verdict == False:
                return 1
                break
        return 0

def pair_ordered(left, right, nest = "") -> bool | None:
    print(nest, "- Compare", left, "vs", right)

    if left == None:
        print(nest, "  ", "- Left side ran out of items, so inputs are in the right order")
        return True
    if right == None:
        print(nest, "  ", "- Right side ran out of items, so inputs are not in the right order")
        return False

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            print(nest, "  ", "- Left side is smaller, so inputs are in the right order")
            return True
        elif left > right:
            print(nest, "  ", "- Right side is smaller, so inputs are not in the right order")
            return False
        else:
            return None

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    
    for l,r in  itertools.zip_longest(left, right):
        verdict = pair_ordered(l,r,f"{nest}  ")
        if verdict == True:
            return verdict
        elif verdict == False:
            return verdict

    return None

def compare(pleft: Packet, pright: Packet) -> int:
    return pleft.compare_with(pright)

def run(input: str):
    packets = input.split('\n\n')
    all_packets =  [Packet(p) for pair in packets for p in pair.split('\n')]
    all_packets.append(Packet("[[2]]"))
    all_packets.append(Packet("[[6]]"))
    s = [l.raw for l in sorted(all_packets, key=functools.cmp_to_key(compare))]
    
    d1 = s.index("[[2]]") + 1
    d2 = s.index("[[6]]") + 1

    print(d1 * d2)






class Tests:

    def test_run(self):
        global test
        test = True
        test_data = open("data_test.txt", 'r').read()
        run(test_data)

if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
