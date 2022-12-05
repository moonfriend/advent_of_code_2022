import re
# read data
stack = []
with open("input05.txt") as input_file:
    l =""
    while True:
        l = input_file.readline()
        if l != "\n": # stack ends by the first empty line
            stack.append(l)
        else:
            break
    # the rest is the procedure orders:
    procedures = input_file.readlines()

# clean the stack into a readable format:
# select the meaningful characters
stack = [s[1:36:4] for s in stack]
# rotate it to have : stack[0] = "items on stack 1"
stack = ["".join([stack[len(stack)-i-2][j].strip() for i in range(len(stack)-1)]) for j in range(len(stack))]

# clean the procedures into readable format
# mov `n` fom `a` to `b` (`-1`s are for matching the zero based indexing in the list)
procedures=[(int(n),int(a)-1,int(b)-1) for _,n,_,a,_,b in [p.split() for p in procedures]]
stack_p2 = stack.copy()
for n,a,b in procedures:
# part 1 calculation happens here
    stack[b] = stack[b] + stack[a][-1:-n-1:-1]
    stack[a] = stack[a][:-n]
# part 2 calculation happens here:
    stack_p2[b] = stack_p2[b] + stack_p2[a][-n:]
    stack_p2[a] = stack_p2[a][:-n]
    
print("top of stack in part 1","".join([s[-1] for s in stack]))
print("top of stack in part 2","".join([s[-1] for s in stack_p2]))

