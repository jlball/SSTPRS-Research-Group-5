#Importing numpy
import numpy as np
import pprint as pp
import copy

#####
#
#   This program generates a text file containing all possible vertex edge matrices for the 36,864 Adinkras from the "adinkra_dict_yangrui.txt" 
#
#####

#Decide how bold you want to be. The number of Adinkras for which to calculate the 16 vertex edge matrices
numOfAdnk = 36864

#loading the .txt file with all of the L matrices for 96 of the 36,864 adinkras
file = np.loadtxt("adinkra_dict_yangrui.txt", dtype=np.int8)

#A function which takes the set of 1x4 numpy arrays of the text file and compiles them into a numpy 4x4 arry
def gLMat(line1, line2, line3, line4):
    matrix = np.array([line1, line2, line3, line4])
    return matrix

#A function for computing the vertex edge matrix for a given configuration of lifted bosons. the 'bosons' argument is a list of four elements, 1, or 0, corresponding to a lift or non lift of that boson
def liftBosons (inputMatrix, bosons):
    VIMatrix = copy.deepcopy(inputMatrix) #Thanks Lawson for fixing this. Weird errors without using this
    for z in range(0, 4):
        if bosons[z] == 1:
            for x in range(0, 16):
                if z == x%4:
                    for y in range(0, 8):
                        VIMatrix[y, x] = - inputMatrix[y, x]
    return VIMatrix


#initialization of the AllL and listOfL matrices for use in the populating of AllL
listOfL = []
AllL = []

#helper variable to handle the index formula correctly
j = 0
for y in range(0, numOfAdnk):
    listOfL = []
    for x in range(0, 4):
        j = x * 4 + y * 16
        listOfL.append(np.transpose(- np.absolute(gLMat(file[j], file[j + 1], file[j + 2], file[j + 3]))))
    AllL.append(listOfL)
#AllL is a python list of python lists, which are each four element lists of numpy 4x4 arrays, which are the individual L matrices
#So AllL is the list of all sets of four L matrices for each adinkra

#generating a 4x16 matrix, which is a concatenation of 4x4 identity matrices, which will become the top four rows of the vertex edge matrix
identity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype = np.int8)
bigIdentity = np.concatenate((identity, identity, identity, identity), 1)

#Initializing the list which will contain all incidence matrices for valise adinkras
AllValiseIncidence = []

#Generating all incidence matrices by concatenating the bigIdentity and the transpose abs value of the L matrices
for x in range(0, numOfAdnk):
    LmatrixPart = np.concatenate((AllL[x][0], AllL[x][1], AllL[x][2], AllL[x][3]), 1, )
    AllValiseIncidence.append(np.concatenate((bigIdentity, LmatrixPart), 0))

#Creating an array which contains all 16 possible raising / lowering combination of Bosons for use in the liftBosons fucntion
allBosonConfigs = np.array([[0, 0, 0, 0],
                                   [1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1],
                                   [1, 1, 0, 0],
                                   [1, 0, 1, 0],
                                   [1, 0, 0, 1],
                                   [0, 1, 0, 1],
                                   [0, 0, 1, 1],
                                   [0, 1, 1, 0],
                                   [1, 1, 1, 0],
                                   [1, 0, 1, 1],
                                   [1, 1, 0, 1],
                                   [0, 1, 1, 1],
                                   [1, 1, 1, 1]
                                   ], dtype=np.int8)

#Initializing a list to store all of the vertex edge matrices with every possible combination of lifted bosons
allIncidence = []

#populating allIncidence using the liftBoson function and iterating through the allBosonConfigs list for each valise vertex edge matrix
for j in range (0, numOfAdnk):
    for i in range (0, 16):
        allIncidence.append(liftBosons(AllValiseIncidence[j], allBosonConfigs[i]))

#For export, np.savetxt needs a 2D array. To generate this we concatenate each element of allIncidence with itself to make one large array
TwoDIncidence = allIncidence[0]
for x in range (1, len(allIncidence)):
    TwoDIncidence = np.concatenate((TwoDIncidence, allIncidence[x]), 0)

print(len(allIncidence))

#exporting the final 2D array of all vertex edge matrices
np.savetxt('Vertex_Edge_Matrices.txt', TwoDIncidence, fmt='%s', delimiter=', ', newline='\n')
