import numpy as np
from scipy.spatial import ConvexHull
from fractions import Fraction
np.set_printoptions(formatter = {'all':lambda x : str(Fraction(x).limit_denominator())})
#自訂def
from GE import *
from FindVertices import *

if __name__ =='__main__':
    ### 確立圖形所在維度
    m = int(input("請輸入所在維度m(輸入型別: 整數, 輸入範圍: m>0)\n "))
    #給定多少點
    n = int(input("請輸入資料數量n(輸入型別: 整數, 輸入範圍: n>0)\n"))
    IsInConv = False
    #stop 0
    #用矩陣存點
    #第1~n-1行分別為x_1,...,x_n
    #第n行為p

    #確立A矩陣
    A = np.mat(np.zeros([n+1,m]))
    #輸入x1,x2,...,xn
    print("請輸入x_1,x_2,...,x_n")
    print("輸入型別: 整數,浮點數,或分數")
    print("輸入範圍:-6.7e+55 < x_ij < 6.7e+55")
    print("兩點距離:d(x,y)>1e-6")
    for i in range(0,n):
        for j in range(0,m):
            A[i,j] = Fraction(input(f'x{i} {j}th element = '))
            #print(A[i,j])
        print()
    ##輸入你要判斷的點
    for i in range(0,m):
        A[n,i]=(Fraction(input(f'p {i}th element = ')))
    #印出A    
    print("A矩陣\n",A)


    #step 1.判斷 p 是否為 x_i
    #看最後一行和前幾行是否一樣
    for i in range(n):
        #判斷是否一樣
        isSame=True 
        for j in range(m):
            if A[n,j]!=A[i,j]:
                isSame=False
                break
        #如果每一項中, 其中一項不一樣,就換行找
        #如果有一項完全一樣, 停止尋找, p為其中一點"
        if isSame:
            print("提示: p其中一點,停止尋找")
            IsInConv = True
            break
    #如果p為其中一點, 結束
    #反之, 開始找頂點"
    if not IsInConv:
        print("提示: p不是其中一點,開始求超平面維度")
        #step 2 確定超平面維度
        #1)以p為基準,把所有點拉到原點上
        for i in range(n):# 先把其他點減p 
            for j in range(m):
                A[i,j] = A[i,j] - A[n,j]
        for j in range(m):# 再把p減p(為零列) 
            A[n,j] = 0
        #print("A",A)
        #2)找出Row(A)的basis
        #用高斯消去法
        R = np.copy(A) #NOTE: 不能用R=A, 因為R動A就會同步動
        R = GE(R)
        #print(A)
        #print(R)
        '''for i in range(n):
            for j in range(m):
                print(R[i,j],end=" ")
            print()'''
        #刪除零列,剩下的列為basis
        for i in range(n,-1,-1):#把0 row 刪除
            isnotZero = False
            for j in range(m):
                #如果第i列有一項為非零數，代表第i列為非零列，停止尋找
                #NOTE: limit_denominator可以找到浮點數R[i,j]的近似值, 目的是為了減少誤差
                if Fraction(R[i,j]).limit_denominator()!=Fraction(0):
                    isnotZero = True
                    break
            #如果第i列為非零列，停止找下一列
            if isnotZero:
                break
            #如果第i列為零列，刪除該列
            R = np.delete(R, i, 0)
        print("R\n",R)

        #3)求rank
        Rank = R.shape[0]
        print("提示: 超平面維度: ",Rank)

        if Rank == m:    #a)如果超平面維度相同, 開始用Quickhull找頂點
            print("提示: 維度剛好, 直接求頂點")
            IsInConv = isVertices(A)
        elif Rank < m:   #b)如果超平面維度太小, 先換成座標, 再用Quickhull求座標的頂點
            print("提示: 維度不足, 換成座標")
            #print("A",A)
            R = R.T
            #print("R",R)
            coordinate = np.mat(np.zeros ([n+1,Rank]))
            # 求 出 座 標
            for i in range(n+1):
                sol = GE_solve ( R ,(A[i,:]).T).T
                coordinate [i ,:]= sol
            # 求 座 標 的 頂 點
            #print(coordinate)
            IsInConv = isVertices(coordinate)
        else:
            raise ValueError('高斯消去法計算錯誤')

    if IsInConv:
        print("p在convex hull裡面")
    else:
        print("p在convex hull外面")