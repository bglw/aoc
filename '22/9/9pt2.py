import re
from collections import defaultdict

class Move:
    def __init__(self, move: str):
        direction, amount = move.split()
        self.amount = int(amount)
        if direction == "R":
            self.direction = [1, 0]
        elif direction == "L":
            self.direction = [-1, 0]
        elif direction == "U":
            self.direction = [0, -1]
        elif direction == "D":
            self.direction = [0, 1]

positions = {"0,0"}
log = set()

class RopeNode:
    def __init__(self, tail: int):
        self.knot = [0, 0]
        self.num = tail
        self.tail = None
        if tail:
            self.tail = RopeNode(tail-1)

    def submove(self, move, parent):
        dist = [abs(x-y) for x,y in zip(self.knot,parent)]
        initial_pos = self.knot
        parent_diag = sum(map(abs, move)) > 1
        if max(dist) > 1:
            if parent_diag and parent[0] == self.knot[0]:
                move[0] = 0
            if parent_diag and parent[1] == self.knot[1]:
                move[1] = 0
            self.knot = [x+y for x,y in zip(self.knot,move)]
            dist = [x-y for x,y in zip(parent,self.knot)]
            if len(log):
                print("Moving", self.num, move, "Parent was", move, "diag:", parent_diag, "Parent dist", dist, "Big", sum(map(abs, dist)) > 1)
                print("- Knot is at", self.knot, "Parent is at", parent)
            if (not parent_diag) and sum(map(abs, dist)) > 1:
                if abs(move[0]):
                    self.knot[1] += dist[1]
                else:
                    self.knot[0] += dist[0]
                if len(log):
                    print("- Adjusted knot to ", self.knot)
            if self.tail:
                moved = [x-y for x,y in zip(self.knot,initial_pos)]
                self.tail.submove(moved, self.knot)
            else:
                positions.add(','.join(map(str, self.knot)))

    def move(self, move):
        for _ in range(move.amount):
            self.knot = [x+y for x,y in zip(self.knot,move.direction)]
            if isinstance(self.tail, RopeNode):
                self.tail.submove(move.direction, self.knot)

    def p(self):
        print(self.num, self.knot)
        if isinstance(self.tail, RopeNode):
            self.tail.p()


def run(input: str):
    positions.clear()
    positions.add("0,0")
    moves = [Move(m) for m in input.splitlines()]
    rope = RopeNode(9)
    for move in moves:
        rope.move(move)
    return len(positions)


class Tests:

    def test_run(self):
        assert run(test_data) == 36
    
    def test_short_run(self):
        assert run(short_test_data) == 1

    def test_parse_move(self):
        move = Move("R 4")
        assert move.amount == 4
        assert move.direction == [1, 0]
    
    def test_move_rope_horiz(self):
        rope = RopeNode(5)

        rope.move(Move("R 4"))
        assert rope.knot == [4, 0]
        assert rope.tail.tail.tail.tail.tail.knot == [0, 0]

        rope.move(Move("U 4"))
        assert rope.knot == [4, -4]
        assert rope.tail.knot == [4, -3]
        assert rope.tail.tail.knot == [4, -2]
        assert rope.tail.tail.tail.knot == [3, -2]
        assert rope.tail.tail.tail.tail.knot == [2, -2]
        assert rope.tail.tail.tail.tail.tail.knot == [1, -1]

        rope.move(Move("R 2"))
        assert rope.knot == [6, -4]
        assert rope.tail.knot == [5, -4]
        assert rope.tail.tail.knot == [5, -3]
        assert rope.tail.tail.tail.knot == [4, -3]
        assert rope.tail.tail.tail.tail.knot == [3, -3]
        assert rope.tail.tail.tail.tail.tail.knot == [2, -2]

        log.add("")
        print("")
        rope.move(Move("D 4"))
        assert rope.knot == [6, 0]
        assert rope.tail.knot == [6, -1]
        assert rope.tail.tail.knot == [6, -2]
        assert rope.tail.tail.tail.knot == [5, -2]
        assert rope.tail.tail.tail.tail.knot == [4, -2]
        assert rope.tail.tail.tail.tail.tail.knot == [3, -2]


# . . . . . . .     -5
# . . . . . . .     -4
# . . . . . . .     -3
# . . . 0 1 2 3     -2
# . . . . . . 4     -1
# . . . . . . 5      0

# 0 1 2 3 4 5 6

    # def test_move_rope_leftward(self):
    #     rope = Rope()
    #     right = Move("R 1")
    #     left = Move("L 1")
    #     for _ in range(4):
    #         rope.move_head(right)
    #     for _ in range(4):
    #         rope.move_head(left)
    #     assert rope.head == [0, 0]
    #     assert rope.tail == [1, 0]

    # def test_move_rope_diag(self):
    #     rope = Rope()
    #     rope.move_head(Move("R 1"))
    #     rope.move_head(Move("U 2"))

    #     assert rope.head == [1, -2]
    #     assert rope.tail == [1, -1]

    # def test_move_rope_down_diag(self):
    #     rope = Rope()
    #     rope.move_head(Move("R 1"))
    #     rope.move_head(Move("D 2"))

    #     assert rope.head == [1, 2]
    #     assert rope.tail == [1, 1]

    # def test_a_bunch_of_moves(self):
    #     rope = Rope()
    #     rope.move_head(Move("R 1"))
    #     rope.move_head(Move("D 2"))

    #     assert rope.head == [1, 2]
    #     assert rope.tail == [1, 1]

    #     rope.move_head(Move("R 2"))
    #     assert rope.head == [3, 2]
    #     assert rope.tail == [2, 2]

    #     rope.move_head(Move("L 2"))
    #     assert rope.head == [1, 2]
    #     assert rope.tail == [2, 2]

    #     rope.move_head(Move("L 2"))
    #     assert rope.head == [-1, 2]
    #     assert rope.tail == [0, 2]

    #     rope.move_head(Move("U 2"))
    #     assert rope.head == [-1, 0]
    #     assert rope.tail == [-1, 1]

    #     rope.move_head(Move("U 10"))
    #     assert rope.head == [-1, -10]
    #     assert rope.tail == [-1, -9]


    # def test_visited(self):
    #     rope = Rope()
    #     rope.move_head(Move("R 1"))
    #     rope.move_head(Move("D 2"))

    #     assert rope.head == [1, 2]
    #     assert rope.tail == [1, 1]

    #     rope.move_head(Move("R 2"))
    #     assert rope.head == [3, 2]
    #     assert rope.tail == [2, 2]

    #     rope.move_head(Move("L 2"))
    #     assert rope.head == [1, 2]
    #     assert rope.tail == [2, 2]

    #     rope.move_head(Move("L 2"))
    #     assert rope.head == [-1, 2]
    #     assert rope.tail == [0, 2]

    #     rope.move_head(Move("U 2"))
    #     assert rope.head == [-1, 0]
    #     assert rope.tail == [-1, 1]

    #     rope.move_head(Move("U 10"))
    #     assert rope.head == [-1, -10]
    #     assert rope.tail == [-1, -9]


test_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

short_test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
