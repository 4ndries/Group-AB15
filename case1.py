import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



xyz=[]
xdat=[]
ydat=[]
zdat=[]

def caseplot(i,xyz=None):
    xyz =[] if xyz is None else xyz
    with open('case1'+str(i)+'.txt','r') as f:
        for line in f:
            splitline=line.split("\t")
            xyz.append([float(splitline[0]),float(splitline[1]),float(splitline[-1])])
            xyz.sort()
        return xyz
count=[]
step=[]
e=5.
def steplist(i,count=None,step=None):
    count=[] if count is None else count
    step=[] if step is None else step
    for j in range(len(xdata(i))):
        for k in range(1,6):
            if j+k<len(xdata(i)):
                if abs(xdata(i)[j+k]-xdata(i)[j])<e:
                    count.append(j)
                    
    step=list(set(np.arange(0,max(count)+1,1))-set(count))
    step.append(0)
    step.append(len(xdata(i)))
    step.sort()
    return step

for i in range(1,9):
    print(steplist(i))


        





















    








        


