class Monkey:
    def __init__(self, data: list, is_game_relievable, verbos=False):
        self.name = data[0]
        self.items = [int(item.strip(",")) for item in data[1].split()[2:]]
        self.operations = self.read_operation(data[2])
        self.test = self.read_test(data[3])
        self.test_true_case = int(data[4].split("If true: throw to monkey")[1].strip())
        self.test_false_case = int(
            data[5].split("If false: throw to monkey")[1].strip()
        )
        self.verbos = verbos
        self.inspections = 0
        self.is_relievable = is_game_relievable
        self.relief_value = None

    def __str__(self):
        return str((self.name, self.items, self.test_true_case, self.test_false_case))

    def read_test(self, test_line):
        self.divisible_by = int(test_line.split("Test: divisible by ")[1])
        test = lambda x: (x % self.divisible_by) == 0
        return test

    def run_test(self, x):
        return self.test_true_case if self.test(x) else self.test_false_case

    def set_peers(self, monkeys):
        self.peers = monkeys

    def send_item(self, item, destination):
        # we are using the index as the address.
        # However the destination is being checked by the receivers receive_item function
        # against the receiver's name
        self.peers[destination].receive_item(item, destination)

    def read_operation(self, operation_line):
        op = operation_line.split("Operation: new = ")[1].split()

        if op[0] == "old":
            op_0 = lambda x: x
        elif op[0].isnumeric():
            op_0 = lambda x: int(op[0])

        if op[2] == "old":
            op_2 = lambda x: x
        elif op[2].isnumeric():
            op_2 = lambda x: int(op[2])

        if op[1] == "*":
            op_1 = lambda x, y: x * y
        elif op[1] == "+":
            op_1 = lambda x, y: x + y
        return op_0, op_1, op_2

    def run_operation(self, old):
        op_0, op_1, op_2 = self.operations
        return op_1(op_0(old), op_2(old))

    def set_relief_value(self, x):
        self.relief_value = x

    def relief(self, x):
        # if value is too big, reduce it
        if self.relief_value:
            x = x % self.relief_value

        result = x // 3 if self.is_relievable else x
        self._log(f"{self.name} gets bored with item, new worry level: {result}")
        return result

    def _log(self, msg):
        if self.verbos:
            print(msg)

    def receive_item(self, items_worry_level, receiver_monkey=None):
        if receiver_monkey:
            assert self.name == f"Monkey {receiver_monkey}:"
        self.items.append(items_worry_level)
        self._log(f"{self.name} receives item: {items_worry_level}")

    def inspect_next(self):
        if len(self.items) == 0:
            return False  # or through an error?
        item_in_hand = self.items.pop(0)
        self._log(f"** {self.name} examines item: {item_in_hand}")
        # new worry level
        item_in_hand = self.run_operation(item_in_hand)
        self._log(f"worry level increases to {item_in_hand}")

        item_in_hand = self.relief(item_in_hand)
        self._log(f"worry level reliefs to {item_in_hand}")

        destination = self.run_test(item_in_hand)

        self._log(
            f"item with worry level {item_in_hand} is gonna be sent to {destination}"
        )

        self.send_item(item_in_hand, destination)
        self.inspections += 1
        return True

    def inspect_items(self):
        while True:
            if not self.inspect_next():
                break

with open("input11.txt") as input_file:
    lines = [l.strip() for l in input_file.readlines()]

# first analyze input
monkeys = []
for i in range(0, len(lines), 7):
    monkeys.append(Monkey(lines[i : i + 7], is_game_relievable=True, verbos=False))
for monkey in monkeys:
    monkey.set_peers(monkeys)
# and run the simulation:
for r in range(20):
    for monkey in monkeys:
        # print(f"next {monkey.name}")
        monkey.inspect_items()

results = [
    f"{monkey.name} `s monkey inspections: {monkey.inspections}" for monkey in monkeys
]
print("\n".join(results))

all_inspections = [monkey.inspections for monkey in monkeys]
all_inspections.sort()
print(f"Part 1: {all_inspections[-1]*all_inspections[-2]}")

############################### part 2
monkeys = []

for i in range(0, len(lines), 7):
    monkeys.append(Monkey(lines[i : i + 7], is_game_relievable=False, verbos=False))

all_divisible_values = [monkey.divisible_by for monkey in monkeys]
multiplied = 1
for i in all_divisible_values:
    multiplied = multiplied * i
print(f"multiplied {multiplied}")

for monkey in monkeys:
    monkey.set_peers(monkeys)
    monkey.set_relief_value(multiplied)


pipi = lambda: print([monkey.items for monkey in monkeys])
for r in range(1, 10001):
    for monkey in monkeys:
        monkey.inspect_items()

    if r in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:

        print(f"round {r}")
        results = [
            f"{monkey.name} `s monkey inspections: {monkey.inspections}"
            for monkey in monkeys
        ]
        print("\n".join(results))

        all_inspections = [monkey.inspections for monkey in monkeys]
        all_inspections.sort()
        print(f"End of round, business: {all_inspections[-1]*all_inspections[-2]}")

