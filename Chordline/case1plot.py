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


def xdata(i,xdat=None):
    xdat=[] if xdat is None else xdat
    for j in caseplot(i):
        xdat.append(j[0])
    return xdat


def ydata(i,ydat=None):
    ydat=[] if ydat is None else ydat
    for j in caseplot(i):
        ydat.append(j[1])
    return ydat

def zdata(i,zdat=None):
    zdat=[] if zdat is None else zdat
    for j in caseplot(i):
        zdat.append(j[2])
    return zdat

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
                    


xav=[]
def xaverage(i,xav=None):
    xav=[] if xav is None else xav
    for j in range(len(steplist(i))):
        if j+1<len(steplist(i)):
            if j!=0:
                a=steplist(i)[j]+1
            else:
                a=steplist(i)[j]
            b=steplist(i)[j+1]+1
            xav.append(sum(xdata(i)[a:b])/(len(xdata(i)[a:b])))
    return xav

yav=[]
def yaverage(i,yav=None):
    yav=[] if yav is None else yav
    for j in range(len(steplist(i))):
        if j+1<len(steplist(i)):
            if j!=0:
                a=steplist(i)[j]+1
            else:
                a=steplist(i)[j]
            b=steplist(i)[j+1]+1
            yav.append(sum(ydata(i)[a:b])/(len(ydata(i)[a:b])))
    return yav

for i in range(1,9):
    print('\n Average case1'+str(i)+' data')
    for j in range(len(xaverage(i))):
        print(round(xaverage(i)[j],5),'  ',round(yaverage(i)[j],5))





        


