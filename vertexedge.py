
import numpy as np
import itertools as itr
import pickle

from os.path import exists

def main():
    working_eight_by_sixteens = get_working_8x16s()
            
    with open("output.txt", "w+") as f:
        for working_eight_by_sixteen in working_eight_by_sixteens:
            f.write(numpy_matrix_pretty(working_eight_by_sixteen) + "\n\n")
            
    with open("output.pickle", "wb") as f:
        pickle.dump(working_eight_by_sixteens, f)
              
        
def get_working_8x16s():
    permutation_matrices = generate_permutation_matrices()
    combinations_of_permutation_matrices = itr.combinations(permutation_matrices, 4) # all size 4 combinations of permutation matrices
    
    working_eight_by_sixteens = []
    for combination in combinations_of_permutation_matrices:
        if add_up_to_one(combination):
            negated_and_transposed_combination = [np.negative(np.transpose(matrix)) for matrix in combination] # transpose and negate each matrix
            working_eight_by_sixteens.extend(permute_around_bottom_4x16(negated_and_transposed_combination))
         
    return working_eight_by_sixteens
        
            
def generate_permutation_matrices():
    permutation_matrices = []
    positions_of_ones = [0, 1, 2, 3]
    
    for position_of_ones in itr.permutations(positions_of_ones): # iterate over all permutations of the above matrix
        matrix = np.zeros((4, 4))
        for i, position in enumerate(position_of_ones):
            matrix[i][position] = 1 # put a 1 in the [position]th column of the [i]th row
            
        permutation_matrices.append(matrix)
        
    return permutation_matrices


def add_up_to_one(list_of_permutation_matrices):
    sum_of_matrices = np.zeros((4, 4))
    
    for matrix in list_of_permutation_matrices:
        sum_of_matrices = np.add(sum_of_matrices, matrix)
    
    return (np.amax(sum_of_matrices) == 1) # if they dont add up to all 1s, there will be a number > 1 in there somewhere


def permute_around_bottom_4x16(list_of_permutation_matrices):
    eight_by_sixteens = []
    for permutation_of_permutation_matrices in itr.permutations(list_of_permutation_matrices):
        eight_by_sixteens.append(np.bmat([[np.identity(4) for i in range(4)], permutation_of_permutation_matrices]))
        
    return eight_by_sixteens


def numpy_matrix_pretty(numpy_matrix):
    ret = ""
    for row in numpy_matrix:
        ret += "|  "
        for element in np.nditer(row):
            if element >= 0:
                ret += " {}  ".format(int(element + 0)) # element + 0 coerces negative zero to zero
            else:                                  # otherwise it looks like ass
                ret += "{}  ".format(int(element + 0))
        ret += "|\n"

    return ret


def recover_working_eight_by_sixteens():
    if exists("output.pickle"):
        with open("output.pickle", "rb") as f:
            return pickle.load(f)
    else:
        working_eight_by_sixteens = get_working_8x16s()
        with open("output.pickle", "wb") as f:
            pickle.dump(working_eight_by_sixteens, f)
        return working_eight_by_sixteens


if __name__ == "__main__":
    main()
