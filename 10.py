
with open("input10.txt") as input_file:
    lines = [l.strip() for l in input_file.readlines()]
   
instruction_costs = {'noop':1, 'addx':2}

class CPU:
    def __init__(self, instructions):
        self.instructions = instructions.copy()
        self.cycle = 0
        self.queue = {} # {"t": Time2Wait, "func", func2Exec}
        self._init_memory()

    def _init_memory(self):
        self.x = 1
        self.x_buf = 1

    def next_cycle(self):
        # we just keep track of the cycle for sanity check
        self._prep_cycle()
        self.cycle = self.cycle + 1
        self._execute_cycle()
        # if anything in cue, execute it

    def _prep_cycle(self):
        # here we read the instructions if needed and set the que to be executed

        if self.queue:
            # nothing to read here
            pass
        else:
            self._prep_instruction()

    def _prep_instruction(self):
        if len(self.instructions)==0:
            raise Exception("cpu ran out of instructions")

        # here we read the next instruction and put it in the queue
        inst = self.instructions.pop(0).split()
        if inst[0] == 'noop':
            self.queue = {}
        elif inst[0] == 'addx':
            addx_func = lambda: self.addx(int(inst[1]))
            self.queue = {"t":2, "func": addx_func}

    def _execute_cycle(self):
        if self.queue:
            self.queue["t"] = (t:=self.queue["t"] -1)
            if t == 0:
                self.queue["func"]()
                self.queue = {}
            elif t < 0:
                raise Exception("crazy cpu error, sounds like we missed a cycle somewhere!")
            else:
                return

    def addx(self, x):
        self.x = self.x + x

class CRT:
    def __init__(self, cpu):
        self.cpu = cpu
        self.pxls = list("." * 240)
        self.PX = 40
        self.PY = 6
        self.sprite = "S"

    @property
    def sploc(self):
        return cpu.x

    def __str__(self):
        # first draw the sprite
        # we don't want the sprite to be actually there, its a ghost after all!

        rows = ["".join(self.pxls[i:i+40]) for i in range(0,len(self.pxls),self.PX)]
        rows.append("0123456789012345678901234567890123456789")
        sp_row = list("." * self.PX)
        for i in [-1, 0, 1]:
            if 0 <= (loc:= self.sploc +i) and loc<self.PX:
                sp_row[loc] = self.sprite
        rows.append("".join(sp_row))
        return "\n".join(rows)

    def _draw_based_on_cycle(self, cycle, ch="#"):
        cycle = cycle -1 # cycle 1 corresponds to pxl 0
        row = int(cycle / self.PX) # edge values: like 39?
        col = cycle % self.PX
        if col in [self.sploc +i for i in [-1,0,1]]:
            self._draw(row * self.PX + col, ch)
    def _draw(self, x, ch):
        self.pxls[x] = ch

    def next_cycle(self, cycle):
        self._draw_based_on_cycle(cycle, "#")
    

# first part
cpu = CPU(instructions=lines)

cycle = 0
cycles_of_interest = [20, 60, 100, 140, 180, 220]
saved_data = {"coi":[]}

while True:
    cycle = cycle + 1 # the clock ticks in every cycle
    if cycle in cycles_of_interest:
        print(f" cycle of interest {cycle} (in cpu: {cpu.cycle}), register is {cpu.x}")
        print(f"signal strength is {cycle * cpu.x}")
        saved_data["coi"].append((cycle, cpu.x))

    try:
        cpu.next_cycle()
    except Exception:
        print("something went wrong in cpu, stopping execution, probably end of instructions")
        break;

sum_ = sum([x*coi for x, coi in saved_data["coi"]])    
print(f"Part 1, sum of signal strengths: {sum_}")

# part 2
cpu = CPU(instructions=lines)
crt = CRT(cpu=cpu)

cycle = 0
while True:
    cycle = cycle + 1 # the clock ticks in every cycle
    crt.next_cycle(cycle)
    try:
        cpu.next_cycle()
    except Exception:
        print("something went wrong in  cpu, stopping execution, probably end of instructions")
        break;

print(crt)

