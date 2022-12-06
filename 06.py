

with open("input06.txt") as input_file:
    lines = input_file.readlines()


assert len(lines)==1 # assuming the input is in one line
line = lines[0]

N = 4 # /14 distinct number of characters
for i, c in enumerate(line.strip()):
    buf = set(line[i:i+N])
    print(i)
    if len(buf)==N:
        print(i)
