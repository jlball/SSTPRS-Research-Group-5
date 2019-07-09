#Importing numpy
import numpy as np
import copy
import pprint as pp

#loading the .txt file with all of the L matrices for 96 of the 36,864 adinkras
file = np.loadtxt("small_library.txt", dtype=np.int8)

#A function which takes the set of 1x4 numpy arrays of the text file and compiles them into a numpy 4x4 array
def gLMat(line1, line2, line3, line4):
    matrix = np.array([line1, line2, line3, line4])
    return matrix


#initialization of the AllL and listOfL matrices for use in the populating of AllL
listOfL = []
AllL = []

#helper variable to handle the index formula correctly
j = 0
for y in range(0, 96):
    listOfL = []
    for x in range(0, 4):
        j = x * 4 + y * 16
        listOfL.append(np.transpose(- np.absolute(gLMat(file[j], file[j + 1], file[j + 2], file[j + 3]))))
    AllL.append(listOfL)
#AllL is a python list of python lists, which are each four element lists of numpy 4x4 arrays, which are the individual L matrices
#So AllL is the list of all sets of four L matrices for each adinkra


#Transpose the L to find the Rs
#np.transpose()
AllR = copy.deepcopy(AllL)

for m in range(96):
    for n in range (4):
        AllR[m][n] = np.transpose(AllL[m][n])

#Define Gizmo

result = np.zeros((96,96))

for i in range(96):
    for j in range(96):
        tempSum = 0

        for w in range(4):
            for x in range(w + 1, 4):

                matrix = np.matmul(AllR[i][w], AllL[i][x])
                matrix = np.matmul(matrix, AllR[j][w])
                matrix = np.matmul(matrix, AllL[j][x])
                        
                tempSum += np.matrix.trace(matrix)


        result[i][j] = (1/24)*tempSum #we found 24 by running the program and using that as the normalization constant

print(result)
'''
def tracepart(i,j,k):
    multiplied = np.matmul(AllR[i][j], AllL[i][k])
    return np.matrix.trace(multiplied)


tempSum = 0

for i in range(1):
    for j in range(4):
        for k in range(4):
            tempSum += tracepart(i,j,k)

Gizmo = (1/48) * tempSum

print(Gizmo)'''
