# read data
def pipi(M):
    for m in M:
        print(m)

with open("input08.txt") as input_file:
    lines = input_file.readlines()
lines_orig = [list(l.strip()) for l in lines]
lines = lines_orig.copy()
# sample:
#lines = lines[0:4]

result_matrix = [[False for item in l] for l in lines]
# True = visible, False = non-visible
# going from the left side

def check_hight_in_forest_from_left(forest, result_matrix):
    assert len(forest) == len(result_matrix)
    assert len(forest[0]) == len(result_matrix[0])

    
    for i,row in enumerate(forest):
        left_high = row[0]
        result_matrix[i][0] = True # edge tree
        for j,c in enumerate(row):
            if c > left_high:
                result_matrix[i][j] = True
                left_high = c # new highest item on the left

def rotate_matrix_90(M, direction=-1):
    ## by default it rotates clock-wise (negative direction)
    # assume matrix
    Xim = len(M) # dimensions
    Yim = len(M[0])
    if direction > 0: 
    # positive or counter clock-wise:
        return [[M[j][Yim-1-i] for j in range(Yim)] for i in range(Xim)]
    else:
    # negative or clock-wise:
        return [[M[Xim-1-j][i] for j in range(Xim)] for i in range(Yim)]

check_hight_in_forest_from_left(lines, result_matrix)
for rotation in [90, 180, 270]:
    result_matrix = rotate_matrix_90(result_matrix)
    lines = rotate_matrix_90(lines)
    check_hight_in_forest_from_left(lines, result_matrix)

print("Answer part 1:", sum([sum(row) for row in result_matrix]))

# part 2
def score_scene_one_direction(forest):
    """forest: a NxM matrix"""
    result_matrix = [[False for item in l] for l in forest]
    for i,row in enumerate(forest):
        for j,t in enumerate(row):
            print(i,j)
            right_side = row[j+1:]
            # find next element bigger than t
            # the default (second line) is for the end of the row
            score = next((x for x, val in enumerate(right_side) if val >= t),
                         0 if right_side==[] else len(right_side)-1) + 1
            # or in human language: if at the end of the row : 0 + 1
            #                       if the rest of the row are shorter: len(rest_of_row) {-1+1}
            result_matrix[i][j] = score
    return result_matrix

# sample data
#ll=["30373","25512","65332","33549","35390"]
lines = lines_orig.copy()
forest=[list(l) for l in lines]
foret_0 = forest.copy()
result_scene_scores_multiplied = [[1 for item in l] for l in forest]

result_matrix_4_directions = []
result_matrix_non_rotated = []
for rotation in [0, 90, 180, 270]:
    result_matrix = score_scene_one_direction(forest)
    result_matrix_non_rotated.append(result_matrix)
#    rotate the result back so the 4 results would be comparable:
    for i in range(int(rotation/90)):
        print("rotated_back_once")
        result_matrix =  rotate_matrix_90(result_matrix, +1)
    result_matrix_4_directions.append(result_matrix)
    # we already multiply them here so that we won't need to go through the loop again
    # to my future if I ever see this again: sorry, I was in zombie mode
    result_scene_scores_multiplied = [[
        result_scene_scores_multiplied[i][j] * result_matrix[i][j] \
        for j in range(len(result_matrix))] \
        for i in range(len(result_matrix))] 
    forest = rotate_matrix_90(forest)

# questions for my doubts: is rotation actually a correct strategy?
import ipdb;ipdb.set_trace()
print("")
