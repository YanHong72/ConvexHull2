import numpy as np
from scipy.spatial import ConvexHull
from fractions import Fraction
from GE import *
np.set_printoptions(formatter = {'all':lambda x : str(Fraction(x).limit_denominator())})

def rank_of_RowSpace(B):
    #dim of RowSpace(A) = rank(A)
    For_Rank = GE(B)#先用高斯

    for i in range(For_Rank.shape[0]-1,-1,-1):#把0 row 刪除
        isZero = False
        for j in range(For_Rank.shape[1]):
            if For_Rank[i,j]!=0:
                isZero = True
                break
        if isZero:
            break
        For_Rank = np.delete(For_Rank, i, 0)
    return For_Rank.shape[0]


def moveToOrigin(B):
    
    r,c = B.shape
    for i in range(1,r):
        for j in range(c):
            B[i,j] = B[i,j] - B[0,j]
    for j in range(c):
        B[0,j] = 0
    #print(B)
    return B
    '''
    R = np.mat(np.zeros([r,c]))#裝移到原點的容器
    for i in range(r):
        for j in range(c):
            R[i,j]=B[0,j]#每一列都放x1
    R = B - R#以x1為基準,移動到原點'''
