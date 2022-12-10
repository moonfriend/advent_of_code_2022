import copy

class GridPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def step(self, direction):
        if direction == "L":
            self.x = self.x - 1
        elif direction == "R":
            self.x = self.x + 1
        elif direction == "D":
            self.y = self.y - 1
        elif direction == "U":
            self.y = self.y + 1
        else:
            raise Exception(f"direction: {direction} not recognized!")

    def _immediate_neighbour(self, point):
        return self.distance(point) <= 1.4143 # ~ (1^2+1^2)^.5

    def distance(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** (1 / 2)

    def four_neighbours(self):
        four_directions = ['L','U','R','D']
        points = [copy.copy(self) for d in four_directions]
        _ = [p.step(d) for p, d in zip(points, four_directions)]

        return points

    def eight_neighbours(self):
        points = [copy.copy(self) for d in range(8)]
        directions = [(1, 0), (1, -1), (1, 1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        for p,d in zip(points, directions):
            p.x = p.x + d[0]
            p.y = p.y + d[1]
        return points

    @property
    def location(self):
        return (self.x, self.y)

    def follow(self, point):
        # we assume that moving for more than one step will break the rope

        if (  # same position or immediate neighbourhood
            self.location == point.location or self._immediate_neighbour(point)
        ):
            return
        # logic: if not neighbourhood: move to the closest place out of eight neighbourhood
        # which are accessible by one step
        else:
            neighbours = point.eight_neighbours()
            # points accessible by one move sqrt(1+1) = ~1.42
            accessible = filter(lambda p: self.distance(p) < 1.42, neighbours) 
            # choose the neighbours which are available within one step
            closest_neighbour_to_go = min(accessible, key=lambda p: point.distance(p))
            self.x, self.y = closest_neighbour_to_go.location


with open("input09.txt") as input_file:
    lines = [l.strip() for l in input_file.readlines()]

head = GridPoint(0, 0)
tail = GridPoint(0, 0)

saved_tail_locations = set()
for l in lines:
    direction, count = l.split()
    for c in range(int(count)):
        head.step(direction)
        tail.follow(head)
        saved_tail_locations.update([tail.location])
print("part one:",len(saved_tail_locations))


# part 2
head = GridPoint(0, 0)
tails = [GridPoint(0,0) for i in range(9)]
saved_tail_locations = set()
for l in lines:
    direction, count = l.split()
    for c in range(int(count)):
        head.step(direction)
        to_follow = head
#       import ipdb;ipdb.set_trace()

        for t in tails:
            t.follow(to_follow)
            to_follow = t
        saved_tail_locations.update([tails[-1].location])

print("part one:",len(saved_tail_locations))

