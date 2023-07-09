import numpy as np
import numpy.random as rn
from scipy.spatial import ConvexHull
from fractions import Fraction


def hullfordim1(A):
    Max = Fraction(A[0,0])
    indexOfMax = 0
    Min = Fraction(A[0,0])
    indexOfMin = 0
    for i in range(A.shape[0]):
        if Max < Fraction(A[i,0]):
            Max = Fraction(A[i,0])
            indexOfMax = i
        if Min > Fraction(A[i,0]):
            Min = Fraction(A[i,0])
            indexOfMin = i
    return [indexOfMin,indexOfMax,]
def isVertices(A,m,n):   
    IsInConv = False
    if m == 1: #特殊情況:如果m=1,只要找最大最小值的位置即可
        vt = hullfordim1(A)
    else: #找哪一列是頂點
        vt = ConvexHull(A).vertices
    print(vt)
    if n in vt:#確定n是否為頂點
        IsInConv=False#是,就不在內
        print("p為頂點")
    else:
        IsInConv=True#否,就在內
        print("p不為頂點")
    return IsInConv