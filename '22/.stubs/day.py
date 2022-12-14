import re
from collections import defaultdict
import tools

test = False
# if test:
#     assert False

def run(input: str):
    return input


class Tests:

    def test_run(self):
        global test
        test = True
        test_data = open("data_test.txt", 'r').read()
        run(test_data)

if __name__ == '__main__':
    main_data = open("data.txt", 'r').read()
    print(run(main_data))
