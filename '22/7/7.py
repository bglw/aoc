import re
from collections import defaultdict

main_data = open("data.txt", 'r').read()


class FS:
    def __init__(self, parent=None):
        self.dirs = defaultdict(FS)
        self.files = defaultdict(File)
        self.parent = parent


class File:
    def __init__(self, filename="Unknown", size=0):
        self.filename = filename
        self.size = size


def run(input: str):
    fs = FS()
    for command in input.splitlines():
        command = parse_command(command)
        if isinstance(command, File):
            add_file(fs, command)
        elif command:
            fs = move_dir(fs, command)
    fs = move_dir(fs, "/")
    return walk_sizes(fs, 100000)


def parse_command(input: str):
    if input.startswith("$ cd "):
        return input.removeprefix("$ cd ")
    file = re.search(
        '(?P<size>\\d+) (?P<file>.+)', input)
    if file:
        return File(file.group('file'), int(file.group('size')))
    return None


def move_dir(fs: FS, newDir: str) -> FS:
    if newDir.startswith("/"):
        while (fs.parent):
            fs = fs.parent
        return fs
    if newDir == "..":
        return fs.parent or fs
    if fs.dirs.get(newDir):
        return fs.dirs.get(newDir) or fs
    subDir = FS(fs)
    fs.dirs[newDir] = subDir
    return subDir


def add_file(fs: FS, file: File):
    fs.files[file.filename] = file


def calc(fs: FS) -> int:
    return sum(map(lambda f: f.size, fs.files.values())) + sum(map(lambda d: calc(d), fs.dirs.values()))


def walk_sizes(fs: FS, cap: int):
    inner_sum = 0
    for dir in fs.dirs.values():
        dir_size = calc(dir)
        if dir_size <= cap:
            inner_sum += dir_size
        inner_sum += walk_sizes(dir, cap)
    return inner_sum


# # # # # # # # # # #
#       TESTS       #
# # # # # # # # # # #
class Tests:

    def test_parse_command(self):
        assert parse_command("$ cd /") == "/"
        assert parse_command("$ ls") == None
        assert parse_command("dir abc") == None
        filecmd = parse_command("123 abc")
        assert isinstance(filecmd, File)
        assert filecmd.filename == "abc"
        assert filecmd.size == 123

    def test_moving_dir(self):
        fs = FS()

        node = move_dir(fs, "a")
        assert node == fs.dirs.get("a")

        node = move_dir(node, "..")
        assert node == fs

        node = move_dir(node, "a")
        node = move_dir(node, "b")
        assert node == fs.dirs["a"].dirs["b"]

        node = move_dir(node, "/")
        assert node == fs

    def test_add_file(self):
        fs = FS()
        node = move_dir(fs, "a")
        file = File("hello", 400)
        add_file(node, file)

        assert file == fs.dirs["a"].files["hello"]

    def test_calc_dir(self):
        fs = FS()
        add_file(fs, File("hello", 400))
        add_file(fs, File("world", 500))
        assert calc(fs) == 900

    def test_recursive_calc_dir(self):
        fs = FS()
        add_file(fs, File("hello", 400))
        add_file(fs, File("world", 500))
        node = move_dir(fs, "a")
        add_file(node, File("another", 100))
        assert calc(fs) == 1000

    def test_run(self):
        assert run(test_data) == 95437


main_data = open("data.txt", 'r').read()
test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


if __name__ == '__main__':
    print(run(main_data))
