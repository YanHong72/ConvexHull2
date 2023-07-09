import numpy as np
from scipy.spatial import ConvexHull
from fractions import Fraction
np.set_printoptions(formatter = {'all':lambda x : str(Fraction(x).limit_denominator())})
#自訂def
from GE import *
from FindVertices import *

### 確立圖形所在維度
m = int(input("維度"))
#給定多少點
n = int(input("幾筆資料"))
IsInConv = False
#stop 0
#用矩陣存點
#第1~n-1行分別為x_1,...,x_n
#第n行為p

#確立A矩陣
A = np.mat(np.zeros([n+1,m]))
#輸入x1,x2,...,xn
for i in range(0,n):
    for j in range(0,m):
        A[i,j] = Fraction(input(f'x{i} {j}th element = '))
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
    for i in range(n):
        for j in range(m):
            A[i,j] = A[i,j] - A[n,j]
    for j in range(m):
        A[n,j] = 0
    #print("A",A)
    #2)找出Row(A)的basis
    #用高斯消去法
    R = np.copy(A)
    R = GE(R)
    #print(A)
    print(R)
    #刪除零列,剩下的列為basis
    for i in range(n,-1,-1):#把0 row 刪除
        isnotZero = False
        for j in range(m):
            if R[i,j]!=Fraction(0):
                isnotZero = True
                break
        if isnotZero:
            break
        R = np.delete(R, i, 0)

    #3)求rank
    Rank = R.shape[0]
    print("提示: 超平面維度: ",Rank)

    if Rank == m:    #a)如果超平面維度相同, 開始用Quickhull找頂點
        print("提示: 維度剛好, 直接求頂點")
        IsInConv = isVertices(A,m,n)
    else:
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
        IsInConv = isVertices(coordinate,Rank,n)


if IsInConv:
    print("p在convex hull裡面")
else:
    print("p在convex hull外面")