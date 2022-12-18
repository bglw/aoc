## Advent of Code 2022

For days >= 16:
```
function 1() { PYTHONDONTWRITEBYTECODE=1 python3 $(basename "$PWD").py $1 }
function 1t() { 1 t $1 }
function 2() { PYTHONDONTWRITEBYTECODE=1 python3 $(basename "$PWD")pt2.py $1 }
function 2t() { 2 t $1 }
```

(`PYTHONDONTWRITEBYTECODE=1` removes the `__pycache__` dir)
