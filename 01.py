

# read data
with open("input01.txt") as input_file:
    lines = input_file.readlines()

# part 1
current_elf_buffer = []
max_elfs = [0]*4 # for the top 3 elves 

lines.append('\n') # to make it consistent with all batches of data
                   # since we are using the \n as a seperator in input data
for l in lines:
    if l == '\n':
        current_elf = sum(current_elf_buffer)
        max_elfs[0] = current_elf
        max_elfs.sort() 
        current_elf_buffer = []
    else:
        current_elf_buffer.append(int(l))
    
print(max_elf)

