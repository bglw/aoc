import re

# [[1, 2], [3, 4]] -> [[1, 3], [2,4]]
def transpose(list_of_lists: list[list]):
    return [list(row) for row in zip(*list_of_lists)]

# "hello-1 there 2" - > [1, 2]
def get_ints(input_string: str) -> list[int]:
    integers = re.findall(r"\d+", input_string)
    return [int(x) for x in integers]

# "hello-1 there 2" - > [-1, 2]
def get_ints_with_neg(input_string: str) -> list[int]:
    integers = re.findall(r"-?\d+", input_string)
    return [int(x) for x in integers]
