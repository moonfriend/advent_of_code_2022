
# read data
with open("input02.txt") as input_file:
    lines = input_file.readlines()

# part one
shape_scores = {'X':1, 'Y':2, 'Z':3}
round_scores = {
    ('A', 'X') : 3,
    ('A', 'Y') : 6,
    ('A', 'Z') : 0,
    ('B', 'X') : 0,
    ('B', 'Y') : 3,
    ('B', 'Z') : 6,
    ('C', 'X') : 6,
    ('C', 'Y') : 0,
    ('C', 'Z') : 3,
}

score = 0
for l in lines:
    a, b = l.split()
    shape_score = shape_scores[b]
    round_score = round_scores[(a,b)]
    print(shape_score, round_score)
    score += shape_score + round_score
    print(score)
print(score)


# part two
# X:lose Y:draw Z:win
shape_scores = {'A':1, 'B':2, 'C':3}
round_scores = {'X':0, 'Y':3, 'Z':6}
my_moves = { #according to strategy guide (hers, result) : mine
    ('A', 'Y' ):'A',
    ('A', 'Z' ):'B',
    ('A', 'X' ):'C',
    ('B', 'X' ):'A',
    ('B', 'Y' ):'B',
    ('B', 'Z' ):'C',
    ('C', 'Z' ):'A',
    ('C', 'X' ):'B',
    ('C', 'Y' ):'C',
}

score =0
for l in lines:
    her_move, strategy_result  = l.split()
    round_score = round_scores[strategy_result]
    my_move = my_moves[(her_move, strategy_result)]
    shape_score = shape_scores[my_move]
    print(shape_score, round_score)
    score += shape_score + round_score
    print(score)
print(score)
