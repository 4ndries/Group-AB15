import math
import numpy as np
import matplotlib.pyplot as plt
import random
dx=0.1
L=15.
c=400
N=1000

x0=[]
y0=[]
with open('case0.txt','r') as f:
    for line in f:
        splitline=line.split("\t")
        x0.append(float(splitline[0]))
        y0.append(float(splitline[1])-3)
flin0=np.poly1d(np.polyfit(x0[4:9],y0[4:9],1))
theta0=np.arctan(flin0[1])
f0=np.poly1d(np.polyfit(x0,y0,3))
TE0=[x0[-1]+L,y0[-1]+L*(np.sin(np.arctan(flin0[1])))]
LE0=[TE0[0]-c,TE0[1]]
x0range=np.arange(x0[0],TE0[0]+dx,dx)
#plt.scatter(x0,y0,c='r')
#plt.scatter(TE0[0],TE0[1],s=100,c='r')
#plt.scatter(LE0[0],LE0[1],s=100,c='r')
#plt.plot(x0range,f0(x0range),linewidth=6,c='r')
#plt.plot([TE0[0],LE0[0]],[TE0[1],LE0[1]],linewidth=4,c='r')
#plt.legend(['case0'])

fulldata=[]
with open('alldata.txt','r') as f:
    for line in f:
        splitline=line.split("\t")
        fulldata.append(splitline)

selection=[]      
for i in range(N):
    selection.append(int(random.uniform(0,len(fulldata)/3)))

selection.sort()
data=[]


for j in selection:
    data.append(fulldata[j*3])
    data.append(fulldata[j*3+1])
    data.append(fulldata[j*3+2])

def casedata(i,x=None,y=None,SN=None):
    x =[] if x is None else x
    y =[] if y is None else y
    SN=[] if SN is None else SN
    k=(i*3)
    for j in data[k]:
        SN.append(float(j))
    for j in data[k+1]:
        x.append(float(j))
    for j in data[k+2]:
        y.append(float(j))
    return [SN,x,y]

       
def f(i):
    return np.poly1d(np.polyfit(casedata(i)[1],casedata(i)[2],3))

def flin(i):
    return np.poly1d(np.polyfit(casedata(i)[1][4:9],casedata(i)[2][4:9],1))

def TE(i):
    return [casedata(i)[1][-1]+L,casedata(i)[2][-1]+(L*np.arctan(flin(i)[1]))]

def alpha(i):
    return np.arctan(flin(i)[1])-theta0

def LE(i):
    return [TE(i)[0]-c*np.cos(alpha(i)),TE(i)[1]-c*np.sin(alpha(i))]

for i in range(int(len(data)/3)):
    xrange=np.arange(min(casedata(i)[1]),max(casedata(i)[1])+dx,dx)
    xlinrange=np.arange((casedata(i)[1][4]),TE(i)[0]+dx,dx)
    #plt.plot(xrange,f(i)(xrange),'--')
    #plt.plot(xlinrange,flin(i)(xlinrange))
    #print('\n case nr '+str(i))
    #print('snapshot nr: ',int(casedata(i)[0][0]))
    #print('angle of attack: ',round(alpha(i)*(180/np.pi),3),' [deg]')
    #print('Trailing Edge',TE(i))
    #print('Leading Edge',LE(i))
    #plt.scatter(casedata(i)[1],casedata(i)[2])
    #plt.scatter(TE(i)[0],TE(i)[1],s=100)
    #plt.scatter(LE(i)[0],LE(i)[1],s=100)
    #plt.plot([TE(i)[0],LE(i)[0]],[TE(i)[1],LE(i)[1]],'--')
plt.grid()
#plt.ylim(530,670)
#plt.show()
time=[]
alfa=[]
for i in range(int(len(data)/3)):
    time.append((casedata(i)[0][0])/100)
    alfa.append(alpha(i)*(180/np.pi))
    plt.scatter((casedata(i)[0][0])/100,(alpha(i)*(180/np.pi)))
    plt.title('Angle of attack')
    plt.xlabel('time [sec]')
    plt.ylabel('angle of attack [deg]')


A=-4.3
w=2*np.pi/2.05
phi=-0.08
c1=0.3

x=np.arange(min(time),max(time)+dx,dx)
def sinusoid(x):
    return A*np.sin(w*x+phi)+c1
plt.plot(x,sinusoid(x))

plt.grid()    
plt.show()


