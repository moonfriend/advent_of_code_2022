
class Container:
    name = None
    _size = 0
    _parent = None

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

    def get_child(self, target_name):
        return self.members[target_name]

    def __init__(self, name, parent):
        self.members = {}
        self.name = name
        self._parent = parent

    def add_child(self, child_name):
        child = Container(child_name, parent=self)
        self.members[child_name] = child
        return child

    @property
    def size(self):
        if self._size:
            return self._size
        else:
            size = sum([obj.size for name, obj in self.members.items()])
            return size

    @size.setter
    def size(self, value:int):
        if not isinstance(value, int):
            raise Exception('size value should be int')
        self._size = value

    @property
    def parent(self):
        return self._parent if self._parent is not None else None

def recursive_size_search(container: Container):
    if len(container.members) == 0:
        # it is a file not a directory
        return []
    else:
        results = [(container.name, container.size)]
        for container_name, container_obj in container.members.items():
            name_size_tuples = recursive_size_search(container_obj)
            if name_size_tuples is None:
                import ipdb;ipdb.set_trace()

            results = results + name_size_tuples
    return results

# read data
with open("input07.txt") as input_file:
    lines = input_file.readlines()

current_dir = None

for l in lines:
    l = l.strip()
    if l.startswith("$ cd"):
        target = l.split()[-1]
        if target == "/":
            # only first time
            if current_dir:
                raise Exception("we were cone in root! we didn't expect to come here agian TODO")
            current_dir = Container(name=target, parent=None)
            root_dir = current_dir
        elif target == "..":
            current_dir = current_dir.parent
        else: # cd somedir
            current_dir = current_dir.get_child(target)

    elif l.startswith("$ ls"):
        pass
    elif l.split()[0].isnumeric(): # its a file!
        child_file = current_dir.add_child(l.split()[1])
        child_file.size = int(l.split()[0])
    elif l.startswith("dir"): # it's a directory
        current_dir.add_child(l.split()[1])

# now we need to do a recursive search and find the items with the size smaller than 100000
# I wrote a function above to recursively search the directories and find the sizes
# this will be a list of tuples (name, size). The rest is piece of cake
# ;just playing with lists:
all_directory_name_sizes = recursive_size_search(root_dir)
sum_of_sizes_less_than100k = sum([b for a,b in all_directory_name_sizes if b<100000])
print("answer part 1:",sum_of_sizes_less_than100k)
print("total size filled aka / :",root_dir.size)
print("rest from 70000000:", 70000000-root_dir.size)
print("needed to be free:", 30000000)
print("needed to empty:", 30000000 -(70000000-root_dir.size))
needed_to_empty = 30000000 -(70000000-root_dir.size)
all_candidates = [(a,b) for a,b in all_directory_name_sizes if b>needed_to_empty]
print("answer part 2:",min([b for a,b in all_candidates]))
