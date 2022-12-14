## Advent of Code 2022

```
alias 1="PYTHONDONTWRITEBYTECODE=1 python3 *pt1.py"
alias 1t="PYTHONDONTWRITEBYTECODE=1 pytest *pt1.py -o log_cli=true -s -p no:cacheprovider"
alias 2="PYTHONDONTWRITEBYTECODE=1 python3 *pt2.py"
alias 2t="PYTHONDONTWRITEBYTECODE=1 pytest *pt2.py -o log_cli=true -s -p no:cacheprovider"
```

- `PYTHONDONTWRITEBYTECODE=1` removes the `__pycache__ dir
- `-p no:cacheprovider` removes the `.cache` dir
- `-o log_cli=true` logs each test run on its own line with a name
- `-s` passes through `print()` statements
