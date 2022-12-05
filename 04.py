import re
# read data
with open("input04.txt") as input_file:
    lines = input_file.readlines()


pairs = [[int(i) for i in re.split(',|-',l.strip())] for l in lines]
overlaps = [(a<=c and d<=b) or (c<=a and b<=d) for a,b,c,d in pairs]
# for partial overlap, it would not be an overlap of start of one set is bigger than the end of the other
semi_overlaps = [not ((b<c) or (d<a)) for a,b,c,d in pairs]

print(sum(overlaps))
print(sum(semi_overlaps))
