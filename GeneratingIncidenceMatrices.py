#Importing numpy
import numpy as np
import pprint as pp

#loading the .txt file with all of the L matrices for 96 of the 36,864 adinkras
file = np.loadtxt("small_library.txt", dtype=np.int8)

#A function which takes the set of 1x4 numpy arrays of the text file and compiles them into a numpy 4x4 arry
def gLMat(line1, line2, line3, line4):
    matrix = np.array([line1, line2, line3, line4])
    return matrix


# def liftBosons (inputMatrix, bosons):
#     VIMatrix = inputMatrix
#     for z in range(0, 4):
#         #print("Boson #: " + str(bosons[z]))
#         if bosons[z] == 1:
#             #print("Lifted")
#             for x in range(0, 16):
#                 if inputMatrix[z, x] == 1:
#                     for y in range(0, 8):
#                         VIMatrix[y, x] = - inputMatrix[y, x]
#     return VIMatrix;

def liftBosons (inputMatrix, bosons):
    # VIMatrix = inputMatrix
    for z in range(0, 4):
        #print("Boson #: " + str(bosons[z]))
        if bosons[z] == 1:
            #print("Lifted")
            for x in range(0, 16):
                if z == x%4:
                    for y in range(0, 8):
                        inputMatrix[y, x] = - inputMatrix[y, x]
    return inputMatrix;


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

#generating a 4x16 matrix, which is a concatenation of 4x4 identity matrices, which will become the top four rows of the vertex edge matrix
identity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype = np.int8)
bigIdentity = np.concatenate((identity, identity, identity, identity), 1)

#Initializing the list which will contain all incidence matrices for valise adinkras
AllValiseIncidence = []

#Generating all incidence matrices by concatenating the bigIdentity and the transpose abs value of the L matrices
for x in range(0, 96):
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

AllVI = AllValiseIncidence
allV = []

# pp.pprint(AllValiseIncidence)
print("")
print("")
print("")
pp.pprint(AllValiseIncidence[0])
# for i in range (0, 16):
#     allV = []
#     allV.append(liftBosons(AllValiseIncidence[0], allBosonConfigs[i]))
#     pp.pprint(allV)
for i in range (0, 16):
    allV = []
    allV.append(liftBosons(AllVI[0], allBosonConfigs[i]))
    pp.pprint(allV)
    print("")
# allV.append(liftBosons(AllValiseIncidence[0], allBosonConfigs[6]))
#allV.append(liftBosons(AllValiseIncidence[0], allBosonConfigs[2]))
pp.pprint(AllValiseIncidence[0])
pp.pprint(allV)
print("")
print("")


#Hmm very interesting
