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

class Rope:
    def __init__(self):
        self.head = [0, 0]
        self.tail = [0, 0]
        self.positions = {"0,0"}

    def move_head(self, move):
        for _ in range(move.amount):
            self.head = [x+y for x,y in zip(self.head,move.direction)]
            dist = [abs(x-y) for x,y in zip(self.head,self.tail)]
            if max(dist) > 1:
                self.tail = [x+y for x,y in zip(self.tail,move.direction)]
                dist = [x-y for x,y in zip(self.head,self.tail)]
                if sum(map(abs, dist)) > 1:
                    if abs(move.direction[0]):
                        self.tail[1] += dist[1]
                    else:
                        self.tail[0] += dist[0]
                self.positions.add(','.join(map(str, self.tail)))

    def grid(self):
        grid = [["." for _ in range(6)] for _ in range(5)]
        for pos in self.positions:
            x,y = map(int,pos.split(','))
            grid[x][y] = "#"
        print('\n'.join([''.join(subgrid) for subgrid in grid]))

def run(input: str):
    moves = [Move(m) for m in input.splitlines()]
    rope = Rope()
    for move in moves:
        rope.move_head(move)
    return len(rope.positions)


class Tests:

    def test_run(self):
        assert run(test_data) == 13
    
    def test_parse_move(self):
        move = Move("R 4")
        assert move.amount == 4
        assert move.direction == [1, 0]
    
    def test_move_rope_horiz(self):
        rope = Rope()
        move = Move("R 1")
        rope.move_head(move)
        assert rope.head == [1, 0]
        assert rope.tail == [0, 0]
        rope.move_head(move)
        assert rope.head == [2, 0]
        assert rope.tail == [1, 0]

    def test_move_rope_leftward(self):
        rope = Rope()
        right = Move("R 1")
        left = Move("L 1")
        for _ in range(4):
            rope.move_head(right)
        for _ in range(4):
            rope.move_head(left)
        assert rope.head == [0, 0]
        assert rope.tail == [1, 0]

    def test_move_rope_diag(self):
        rope = Rope()
        rope.move_head(Move("R 1"))
        rope.move_head(Move("U 2"))

        assert rope.head == [1, -2]
        assert rope.tail == [1, -1]

    def test_move_rope_down_diag(self):
        rope = Rope()
        rope.move_head(Move("R 1"))
        rope.move_head(Move("D 2"))

        assert rope.head == [1, 2]
        assert rope.tail == [1, 1]

    def test_a_bunch_of_moves(self):
        rope = Rope()
        rope.move_head(Move("R 1"))
        rope.move_head(Move("D 2"))

        assert rope.head == [1, 2]
        assert rope.tail == [1, 1]

        rope.move_head(Move("R 2"))
        assert rope.head == [3, 2]
        assert rope.tail == [2, 2]

        rope.move_head(Move("L 2"))
        assert rope.head == [1, 2]
        assert rope.tail == [2, 2]

        rope.move_head(Move("L 2"))
        assert rope.head == [-1, 2]
        assert rope.tail == [0, 2]

        rope.move_head(Move("U 2"))
        assert rope.head == [-1, 0]
        assert rope.tail == [-1, 1]

        rope.move_head(Move("U 10"))
        assert rope.head == [-1, -10]
        assert rope.tail == [-1, -9]


    def test_visited(self):
        rope = Rope()
        rope.move_head(Move("R 1"))
        rope.move_head(Move("D 2"))

        assert rope.head == [1, 2]
        assert rope.tail == [1, 1]

        rope.move_head(Move("R 2"))
        assert rope.head == [3, 2]
        assert rope.tail == [2, 2]

        rope.move_head(Move("L 2"))
        assert rope.head == [1, 2]
        assert rope.tail == [2, 2]

        rope.move_head(Move("L 2"))
        assert rope.head == [-1, 2]
        assert rope.tail == [0, 2]

        rope.move_head(Move("U 2"))
        assert rope.head == [-1, 0]
        assert rope.tail == [-1, 1]

        rope.move_head(Move("U 10"))
        assert rope.head == [-1, -10]
        assert rope.tail == [-1, -9]


test_data = """R 4
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
