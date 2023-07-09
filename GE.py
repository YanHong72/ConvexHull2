import numpy as np
from scipy.spatial import ConvexHull
from fractions import Fraction
np.set_printoptions(formatter = {'all':lambda x : str(Fraction(x).limit_denominator())})

def GE(A):
    B = np.copy(A)
    rw,cl = B.shape
    curR = 0
    curC = 0
    while(curR<rw and curC<cl):
        #print("curC: ",curC,"curR: ",curR)
        maxEc = abs(B[curR,curC])
        maxRow = curR
        for k in range(curR+1,rw):
            if abs(B[k,curC])> maxEc:
                maxEc = abs(B[k,curC])
                maxRow = k
        B[[curR, maxRow]] = B[[maxRow, curR]]
        #A[[curR,maxRow],curC:] = A[[maxRow,curC],curC:]
        #A[[curR,maxRow],curC:] = A[[curC,maxRow],curC:]
        #print('c',A)
        if(B[curR,curC]!=0):
            for k in range(curR+1,rw):
                c = -(B[k,curC])/B[curR,curC]
                B[k,curC:]=B[k,curC:]+c*B[curR,curC:]
            B[curR,curC:]=(1/B[curR,curC])*B[curR,curC:]
            curR+=1
        curC+=1
        #print('d',curC,A)
    return B

def GE_solve(A,b):
    r = A.shape[0]
    c = A.shape[1]
    CL = np.mat(np.zeros([r,c+1]))
    CL[:,:c] = A
    CL[:,c] = b

    #print("CL",CL)
    #print(GE(CL))
    CL = GE(CL)
    #print("gCL",CL)
    sol =np.zeros([c,1])
    for i in range(c-1,-1,-1):
        sol[i,0]=(CL[i,c])
            
        for j in range(c-1,i,-1):       
            sol[i,0] = sol[i,0] - CL[i,j]*sol[j,0]

    return (sol)