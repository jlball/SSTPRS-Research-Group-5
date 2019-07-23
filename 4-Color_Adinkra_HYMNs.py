#Importing numpy
import numpy as np
import pprint as pp
import copy

file = np.loadtxt("small_library.txt", dtype=np.int8)
#file2 = np.loadtxt("adinkra_dict_yangrui.txt", dtype=np.int8)

def gLMat(line1, line2, line3, line4):
    matrix = np.array([line1, line2, line3, line4])
    return matrix


#Transposing the L-matrices to receive the R-matrices and inserting them into
#the array in alternating order (L_1, R_1, L_2, ..., R_).
def createLandRMatrixList(L_Matrices):
    L_and_R_Matrices = L_Matrices
    for i in range(0, len(L_Matrices)):
        L_and_R_Matrices.insert(4-i, L_Matrices[3-i].transpose())
    return L_and_R_Matrices

#Creating both B-matrices according to the definitions found in the 1904.01738
#paper on pages 10 and 11. (B_L = L_N*R_N-1*...*R_1, B_R = R_N*L_N-1*...*L_1,
#where * is matrix multiplication.)

#Because we are dealing with four color adinkras, the B-matrix will have
#elements in the top left and bottom right, i.e. B_L and B_R, with zeroes
#in the other spaces.
def createBMatrices(L_and_R_Matrices):
    B_L = np.eye(4)
    #B_L_Components = [ ]
    increment = 0
    for i in range(1, len(L_and_R_Matrices)/2+1):
        B_L = np.dot(L_and_R_Matrices[i+increment], B_L)
        #B_L_Components.append(L_and_R_Matrices[i+increment])
        if i%2 is 0:
            increment += 2
    B_R = np.eye(4)
    #B_R_Components = [ ]
    increment = 0
    for i in range(0, len(L_and_R_Matrices)/2):
        B_R = np.dot(L_and_R_Matrices[i+increment], B_R)
        #B_R_Components.append(L_and_R_Matrices[i+increment])
        if i%2 is 0:
            increment += 2
    #return [B_L, B_R, B_L_Components, B_R_Components]
    return [B_L, B_R]

#Finding both the eigenvalues and eigenvectors of the B-matrices. In this algo-
#rithm, only the eigenvalues are returned, which are the HYMN's, but the eigen-
#vectors can be found and returned in the eigenInfo array.
def findHYMNs(B_Matrices):
    HYMN_L = np.linalg.eig(B_Matrices[0])
    HYMN_R = np.linalg.eig(B_Matrices[1])
    eigenInfo = [HYMN_L, HYMN_R]
    HYMNs = [ ]
    #return [HYMN_L, HYMN_R]
    for i in range(0, len(eigenInfo)):
        HYMNs.append(eigenInfo[i][0])
    return HYMNs

#Use this space to instantiate an example set of four L-matrices.
#L_1 = np.array([[1, 0, 0, 0], [0, 0, 0, -1], [0, 1, 0, 0], [0, 0, -1, 0]])
#L_2 = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 0], [0, 0, 0, -1]])
#L_3 = np.array([[0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, -1], [1, 0, 0, 0]])
#L_4 = np.array([[0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0]])

#This line stores the set of L-matrices together in one array.
#L_Matrices = [L_1, L_2, L_3, L_4]

#Instantiating a new array of both L- and R-matrices.
#L_and_R_Matrices = createLandRMatrixList(L_Matrices)

#B_Matrices = createBMatrices(L_and_R_Matrices)

#print(findHYMNs(B_Matrices))

AllL = [ ]
AllAbsoluteL = [ ]

numRepresentedMatrices = len(file)/16

j = 0
for y in range(0, numRepresentedMatrices):
    listOfL = []
    AbsolutelistOfL = []
    for x in range(0, 4):
        j = x * 4 + y * 16
        #listOfL.append(np.transpose(- np.absolute(gLMat(file[j], file[j + 1], file[j + 2], file[j + 3]))))
        listOfL.append(((gLMat(file[j], file[j + 1], file[j + 2], file[j + 3]))))
        AbsolutelistOfL.append((np.absolute(gLMat(file[j], file[j + 1], file[j + 2], file[j + 3]))))
    AllL.append(listOfL)
    AllAbsoluteL.append(AbsolutelistOfL)

AllHYMNs = [ ]
AllAbsoluteHYMNs = [ ]

for z in range(0, len(AllL)):
    L_Matrices = [AllL[z][0], AllL[z][1], AllL[z][2], AllL[z][3]]
    L_and_R_Matrices = createLandRMatrixList(L_Matrices)
    B_Matrices = createBMatrices(L_and_R_Matrices)
    AllHYMNs.append(findHYMNs(B_Matrices))

    Absolute_L_Matrices = [AllAbsoluteL[z][0], AllAbsoluteL[z][1], AllAbsoluteL[z][2], AllAbsoluteL[z][3]]
    Absolute_L_and_R_Matrices = createLandRMatrixList(Absolute_L_Matrices)
    Absolute_B_Matrices = createBMatrices(Absolute_L_and_R_Matrices)
    AllAbsoluteHYMNs.append(findHYMNs(Absolute_B_Matrices))

for v in range(0, len(AllHYMNs)):
    print(AllHYMNs[v])

for w in range(0, len(AllHYMNs)):
    print(AllAbsoluteHYMNs[w])
