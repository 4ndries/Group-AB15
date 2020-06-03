import math
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors
import scipy as sp

dx=0.01
L=15.
c=400
x_c=0.75

LH=18.91814314867475

x0=[]
y0=[]
with open('case0.txt','r') as f:
    for line in f:
        splitline=line.split("\t")
        x0.append(float(splitline[0]))
        y0.append(float(splitline[1])-3)

flin0=np.poly1d(np.polyfit(x0[4:9],y0[4:9],1))
f0=np.poly1d(np.polyfit(x0,y0,3))
TE0=[x0[-1]+L,y0[-1]+L*(np.sin(np.arctan(flin0[1])))]
LE0=[TE0[0]-c,TE0[1]]
H0=[LE0[0]+c*(x_c),TE0[1]]

theta0=np.arctan((y0[4]-y0[0])/(x0[4]-x0[0]))

x0range=np.arange(x0[0],TE0[0]+dx,dx)

print('select analysis of case1 or case2')
print('type: 1 or 2)')
CaseSelection=int(input())
fulldata=[]
with open('case'+str(CaseSelection)+'data.txt','r') as f:
    for line in f:
        if CaseSelection==1:
            splitline=line.split(" ")
        if CaseSelection==2:
            splitline=line.split("\t")
            
        fulldata.append(splitline)


N=int(len(fulldata)/3)
print(N,'Amount of case'+str(CaseSelection)+' snapshots selected')
print('plotting data......')
print(' ')
selection=random.sample((range(0,int(len(fulldata)/3))),N)

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
    return np.poly1d(np.polyfit(casedata(i)[1][0:6],casedata(i)[2][0:6],3))

def H(i):
    return [casedata(i)[1][4]+15,(f(i)(casedata(i)[1][4]+15))]

def flapdata(i,flapx=None, flapy=None):
    flapx=[] if flapx is None else flapx
    flapy=[] if flapy is None else flapy   
    for j in range(len(casedata(i)[1])):
        if j>=5:
            flapx.append(casedata(i)[1][j])
            flapy.append(casedata(i)[2][j])
    flapx.append(H0[0])
    flapy.append(H(i)[1])
    return np.poly1d(np.polyfit(flapx,flapy,1))

def TE(i):
    return [casedata(i)[1][-1]+L,casedata(i)[2][-1]+(L*np.arctan(flapdata(i)[1]))]


def theta(i):
    return np.arctan((casedata(i)[2][4]-casedata(i)[2][0])/(casedata(i)[1][4]-casedata(i)[1][0]))

def alpha(i):
    return theta0-(theta(i))

def sinusoid(x,A,w,phi,c1):
    return A*np.sin(w*x+phi)+c1

def H_chord(i):
    return [H(i)[0]+LH*np.sin(alpha(i)),H(i)[1]+LH*np.cos(alpha(i))]

def LE(i):
    return [H_chord(i)[0]-(c*x_c)*np.cos(alpha(i)),H_chord(i)[1]+(c*x_c)*np.sin(alpha(i))]

def delta(i):
    return -(np.arctan((TE(i)[1]-H_chord(i)[1])/(TE(i)[0]-H_chord(i)[0]))+alpha(i))


 
Tsnps=255
degs=180/(np.pi)
def period(i,periodtab=None,alphatab=None,deltatab=None):
    periodtab=[] if periodtab is None else periodtab
    alphatab=[] if alphatab is None else alphatab
    deltatab=[] if deltatab is None else deltatab
    for j in range(N):
        if casedata(j)[0][0]<(Tsnps*i) and casedata(j)[0][0]>=(Tsnps*(i-1)):
            if i!=1:
                periodtab.append(((casedata(j)[0][0]-Tsnps*(i-1))/100))
                alphatab.append(alpha(j)*degs)
                deltatab.append(delta(j)*degs)
            if i==1:
                periodtab.append(((casedata(j)[0][0])/100))
                alphatab.append(alpha(j)*degs)
                deltatab.append(delta(j)*degs)
    return [periodtab, alphatab, deltatab]





colors=['black','red','gold','darkgreen','darkcyan','navy','m',
        'gray','tan','olive','royalblue','yellowgreen',
        'coral','catedblue','violet']

plt.figure(1)
if CaseSelection==2:
    plt.subplot(211)
    plt.grid()
    plt.title('Case'+str(CaseSelection)+' angle of attack periods')
    plt.yticks(np.arange(-5,5,1))
    plt.xlabel('time [sec]')
    plt.ylabel('Angle of Attack [deg]')

    for i in range(1,16):
        plt.scatter(period(i)[0],period(i)[1],0.8,marker='s')
     



            
        





    
                
    plt.subplots_adjust(hspace=0.7)
    plt.subplot(212)
    for i in range(1,16):
        plt.scatter(period(i)[0],period(i)[2],0.8,marker='s')
    
    plt.xlabel('time [sec]')
    plt.ylabel('Flap deflection angle [deg]')
    plt.title('Case'+str(CaseSelection)+' flap deflection periods')




        
    plt.yticks(np.arange(-8,10,2))
    plt.grid()
    plt.show()

if CaseSelection==1:
    plt.subplot(211)
    plt.grid()
    plt.title('Case'+str(CaseSelection)+' angle of attack periods')
    plt.yticks(np.arange(-5,5,1))
    plt.xlabel('time [sec]')
    plt.ylabel('Angle of Attack [deg]')
    for i in range(1,16):
        plt.scatter(period(i)[0],period(i)[1],0.8,marker='s')
     


    plt.show()

    




