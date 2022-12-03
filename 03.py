
# read data
with open("input03.txt") as input_file:
    lines = input_file.readlines()


#scoring rules
# since I don't want to type them in, I am gonna produce them
lower_case = list(range(ord('a'),ord('z')+1))
upper_case = list(range(ord('A'),ord('Z')+1))
lower_case_prios = {chr(c):s for (c,s) in zip(lower_case,[*range(1,26+1)])}
upper_case_prios = {chr(c):s for (c,s) in zip(upper_case,[*range(27,52+1)])}
prio_rules = {**lower_case_prios, **upper_case_prios}

# part 1
common_elements = []
for ll in lines:
    l = ll.strip()
    midl = int(len(l)/2)
    l1 = l[0:midl]
    l2 = l[midl:]
    common_element = [c for c in l1 if c in l2]

    # sanity check that all shared elements are the same
    assert all(c==common_element[0] for c in common_element)

    common_elements.append(common_element[0])
print(common_elements)
prios = [prio_rules[elem] for elem in common_elements]
print(f"sum: {sum(prios)}")

# part 2

matched_items = []
n = 3 # number of elves in a group
for i in range(0,len(lines), n):
    l1, l2, l3 = [l.strip() for l in lines[i:i+n]]
    # we take the items of one pack and see which item is repeated in the two others
    matched_item = [item for item in l1 if item in l2 and item in l3]
    # sanity check: if it has more than one item, they should be the same at least
    assert all(c==common_element[0] for c in common_element)
    
    matched_items.append(matched_item[0])

    print(matched_items)
    badge_prios = [prio_rules[elem] for elem in matched_items]
    print(f"sum for badges: {sum(badge_prios)}")
