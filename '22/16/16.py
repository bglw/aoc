import re
import sys
import itertools


test = len(sys.argv) > 1 and sys.argv[1].startswith("t")
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()

# Today's solution isn't great, but I don't have the stamina to improve it
# Solving part two takes me ~40s through pypy, but hasn't particularly been optimized
# For now, I'm happy to have a solution at all 😅
# I'm sure there are some memoization quick wins that could be implemented.

# Parsing the input into our graph of valves
valves = {}
for line in lines:
    parse = re.search(
        'Valve (?P<valve>\\w+) has flow rate=(?P<flow>\\d+); tunnels? leads? to valves? (?P<next>.+)', line)
    assert parse != None
    name = parse.group("valve")
    valve = {
        "valve": "_"+name,
        "flow": int(parse.group("flow")),
        "next": parse.group("next").split(', '),
    }
    # For valves with a nonzero flow rate, we create a second room with the same edges, but containing that flow rate,
    # so you can go from AA to _AA for the "opening valve" action. This makes traversal a little easier (for me) since
    # the time aspect can be ignored (all edges cost 1)
    if valve["flow"] > 0:
        valves["_"+name] = valve.copy()
        valve["next"].append("_"+name)
    valve["valve"] = name
    valve["flow"] = 0
    valves[name] = valve


def score_nodes(start, nodes, already_opened=[], time=1):
    # Something like a scored BFS
    # (I guess? I don't exactly know what this is, inspired by something like a djikstra)
    # Used as-is for part one, and with the already_opened constraint for part 2

    notes = {}
    best = 0
    valve = valves[start]
    q: list[tuple[str, int, list[str], int]] = [
        (n, 1, [], 0) for n in valve["next"]]

    while len(q):
        node, depth, chain, prescore = q.pop(0)
        if depth > time:
            continue
        if node not in nodes or node in already_opened:
            continue
        valve = valves[node]
        score = valve["flow"] * (time-depth)
        if node in chain:
            # We have visited this node before in our current chain, thus we have opened it (if it is a valve), returning here has no value
            score = 0
        score += prescore
        if node in notes and notes[node]["score"] >= score:
            # We have noted down a way to get to this node with a higher total score, so the path we're exploring is useless
            continue
        notes[node] = ({"node": node, "score": score,
                        "chain": chain})
        best = max(best, score)
        chain = chain.copy()
        chain.append(node)
        for n in valve["next"]:
            # Explore the next links in this chain (BFS)
            q.append((n, depth + 1, chain, score))

    # Return the highest score that could be attained for a journey of length time
    return best


print("Part 1:", score_nodes("AA", valves.keys(), time=30))

# Build a list containing only the nodes in our graph that represent
# opening a valve (and thus the only nodes with scores)
openable = []
for k in valves.keys():
    if k.startswith("_"):
        openable.append(k)

topscore = 0
for run in range(len(openable)//2):
    # Generate two sets of balanced permutations for the valves that each entity could open
    # (Balanced in the sense that if there are 10 valves and p opens 8, e should open 2)
    # Assumed that the optimal solution will involve every valve being opened
    p_walks = list(itertools.combinations(openable, run+1))
    e_walks = list(itertools.combinations(openable, len(openable)-run-1))

    for p_skip in p_walks:
        for e_skip in e_walks:
            if len(set(p_skip) & set(e_skip)):
                # If both entities are skipping a common valve, bail
                # If this check passes, we know both entites are opening a unique set of valves
                continue
            p_score = score_nodes("AA", valves.keys(), p_skip, time=26)
            e_score = score_nodes("AA", valves.keys(), e_skip, time=26)

            topscore = max(topscore, p_score + e_score)

print("Part 2:", topscore)
