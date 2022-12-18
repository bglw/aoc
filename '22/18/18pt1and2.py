import os

test = 'AOC_TEST' in os.environ
file = "data_test.txt" if test else "data.txt"
input = open(file, 'r').read()
lines = input.splitlines()

cubes = set([tuple([int(x) for x in line.split(',')]) for line in lines])


def exposed_sides(cube):
    exposed = 0
    for x, y, z in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
        side = (cube[0]+x, cube[1]+y, cube[2]+z)
        if side not in cubes:
            exposed += 1
    return exposed


print("Part 1:", sum([exposed_sides(cube) for cube in cubes]))

# Boundaries
minx = min([x for x, _, _ in cubes])-1
maxx = max([x for x, _, _ in cubes])+1

miny = min([y for _, y, _ in cubes])-1
maxy = max([y for _, y, _ in cubes])+1

minz = min([z for _, _, z in cubes])-1
maxz = max([z for _, _, z in cubes])+1

edges = set()
visited = set()

pts = [(minx, miny, minz)]
while len(pts):
    pt = pts.pop(0)
    if pt[0] < minx or pt[0] > maxx or pt[1] < miny or pt[1] > maxy or pt[2] < minz or pt[2] > maxz:
        # Out of bounds, no cubes to be found here
        continue
    if pt in visited:
        continue
    visited.add(pt)
    for x, y, z in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
        side = (pt[0]+x, pt[1]+y, pt[2]+z)
        if side in cubes:
            # Mark this edge as part of the surface area (including the side we're looking from)
            edges.add(pt + tuple("-") + side)
        else:
            pts.append(side)

print("Part 2:", len(edges))
