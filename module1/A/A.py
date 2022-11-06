import fileinput
import re

total = 0
for line in fileinput.input():
    total += sum(map(int, re.findall(r'[-+]?\d+', line)))
print(total)


