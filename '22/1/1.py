log = open("data.txt", 'r')
elves, elf = [], 0

for snack in log.readlines():
    if len(snack.strip()):
        elf += int(snack.strip())
    else:
        elves.append(elf)
        elf = 0

if elf:
    elves.append(elf)

print(max(elves))

elves.sort()
elves.reverse()
print(sum(elves[0:3]))
