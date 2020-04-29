import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
dx=0.01
def caseplot(i,xyz=None):
    xyz =[] if xyz is None else xyz
    with open('case1'+str(i)+'av.txt','r') as f:
        for line in f:
            splitline=line.split("\t")
            xyz.append([float(splitline[0]),float(splitline[1])])
            xyz.sort()
        return xyz
x0=[]
y0=[]
with open('case0.txt','r') as f:
        for line in f:
            splitline=line.split("\t")
            x0.append(float(splitline[0]))
            y0.append(float((splitline[1])))

xdat=[]   

def xdata(i,xdat=None):
    xdat=[] if xdat is None else xdat
    for j in caseplot(i):
        xdat.append(j[0])
    return xdat

ydat=[]
def ydata(i,ydat=None):
    ydat=[] if ydat is None else ydat
    for j in caseplot(i):
        ydat.append(j[1])
    return ydat

def flin(i):
    return np.poly1d(np.polyfit(xdata(i)[4:len(xdata(i))],ydata(i)[4:len(ydata(i))],1))

def flin0(i):
    return np.poly1d(np.polyfit(x0[i:len(x0)],y0[i:len(y0)],1))
alfa0=(flin0(4)[1])


TE=[-466.622,611.087]
LE=[-866.698,612.206]
X=[-466.622,-866.698]
Y=[611.087,612.206]
L=15


theta=[]
for i in range(1,9):
    theta.append(np.arctan(flin(i)[1]))

alfa=[]
for i in range(len(theta)):
    alfa.append((theta[i]-alfa0)*180/np.pi)
snapshots=[0.,500,1000,1500,2000,2500,3000,3500]

plt.scatter(snapshots,alfa,c='r')
plt.grid()
plt.title('Snapshots Case1 angle of attack data ')
plt.xlabel('snapshot nr')
plt.ylabel('angle of attack [deg]')
plt.show()
    
TEtab=[]
for i in range(1,9):
    TEtab.append([xdata(i)[-1]+(L*np.cos(theta[i-1])),ydata(i)[-1]+L*np.sin(theta[i-1])])

plt.title('Case11-18 average xy data plots')
plt.xlabel('x')
plt.ylabel('y')
legend=['case0']
colors=['b','g','r','c','m','y','k','brown']
xrange=np.arange(-719,-477,0.1)
plt.scatter(x0,y0,c='grey')
f0=np.poly1d(np.polyfit(x0,y0,4))
plt.scatter(TE[0],TE[1],c='grey',s=100)
plt.scatter(LE[0],LE[1],c='grey',s=100)
plt.plot(X,Y,c='grey',linewidth=4)


def f(i):
    return np.poly1d(np.polyfit(xdata(i),ydata(i),3))



plt.plot(xrange,f0(xrange),c='grey',linewidth=3)

for i in range(1,9):
    plt.scatter(TEtab[i-1][0],TEtab[i-1][1],c=colors[i-1],s=100)
    #print('\n averages case1'+str(i))
    for j in range(len(caseplot(i))):
        #print(caseplot(i)[j])
        plt.scatter(caseplot(i)[j][0],caseplot(i)[j][1],c=colors[i-1])
    plt.plot(xrange,f(i)(xrange),'--',c=colors[i-1])
plt.legend(legend)
plt.ylim(500,700)
plt.show()
