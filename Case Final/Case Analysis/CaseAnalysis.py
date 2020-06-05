import math
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors
import scipy as sp


dx=0.1
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
print('calulating curve fit of alpha and delta......')
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

plt.figure(1)
if CaseSelection==2:
    plt.subplot(211)
    plt.title('Case'+str(CaseSelection)+' angle of attack recontruction')
    plt.xlabel('time [sec]')
    plt.ylabel('Angle of Attack [deg]')
    plt.subplot(211).set_yticks(np.arange(-6,6,1))
    plt.ylim(-6,6)
    xtab=[]
    alphatab=[]
    deltatab=[]
    x=np.arange(0,(casedata(N-1)[0][0]/100)+dx,dx)
    for i in range(N):  
        plt.scatter((casedata(i)[0][0]/100),alpha(i)*(180/np.pi),0.8,marker='s')
        xtab.append((casedata(i)[0][0]/100))
        alphatab.append(alpha(i)*(180/np.pi))
        deltatab.append(delta(i)*(180/np.pi))


    from scipy.optimize import curve_fit
    alphafit=curve_fit(sinusoid,xtab,alphatab,p0=[4.,2*np.pi/2.5,0,0])
    deltafit=curve_fit(sinusoid,xtab,deltatab,p0=[-8.,2*np.pi/2.5,0,0])
    plt.plot(x,sinusoid(x,alphafit[0][0],alphafit[0][1],alphafit[0][2],alphafit[0][3]))

    def alpha_MSE(x,y):
        return ((y-sinusoid(x,alphafit[0][0],alphafit[0][1],alphafit[0][2],alphafit[0][3]))**2)

    def delta_MSE(x,y):
        return ((y-sinusoid(x,deltafit[0][0],deltafit[0][1],deltafit[0][2],deltafit[0][3]))**2)

    Alphamean=sum(alphatab)/N
    Deltamean=sum(deltatab)/N

    SSRalpha=0.
    SSRdelta=0.
    SSTalpha=0.
    SSTdelta=0.

    for i in range(len(xtab)):
        SSRalpha=SSRalpha+alpha_MSE(xtab[i],alphatab[i])
        SSTalpha=SSTalpha+(alphatab[i]-Alphamean)**2
        SSRdelta=SSRdelta+delta_MSE(xtab[i],deltatab[i])
        SSTdelta=SSTdelta+(deltatab[i]-Deltamean)**2

    alphaRsqd=1-(SSRalpha)/(SSTalpha)
    deltaRsqd=1-(SSRdelta)/(SSTdelta)
    plt.legend([('Function fit R-squared=',round(alphaRsqd,10))],prop={'size':6},loc='upper right')

    print('Angle of attack fit curve')
    print('Alpha= ',round(alphafit[0][0],3),'sin(',round(alphafit[0][1],3),'t  ',round(alphafit[0][2],3),') +',round(alphafit[0][3],3))
    print('R-squared value: ',round(alphaRsqd,6))
    print('\n Flap angle fit curve')
    print('Delta= ',round(deltafit[0][0],3),'sin(',round(deltafit[0][1],3),'t + ',round(deltafit[0][2],3),') +',round(deltafit[0][3]),3)
    print('R-squared value: ',round(deltaRsqd,6))

    print('plotting alpha and delta curves....')
    plt.subplots_adjust(hspace=0.5)
    plt.subplot(212)
    for i in range(N):
        plt.scatter((casedata(i)[0][0]/100),delta(i)*(180/np.pi),0.8,marker='s')
    plt.title('Case'+str(CaseSelection)+' Flap angle recontruction')

        
    plt.plot(x,sinusoid(x,deltafit[0][0],deltafit[0][1],deltafit[0][2],deltafit[0][3]))
    plt.ylim(-10,10)
    plt.xlabel('time [sec]')
    plt.ylabel('Flap angle [deg]')
    plt.legend([('Function fit R-squared=',round(deltaRsqd,10))],prop={'size':6},loc='upper right')

    plt.show()

if CaseSelection==1:
    plt.title('Case'+str(CaseSelection)+' angle of attack recontruction')
    plt.xlabel('time [sec]')
    plt.ylabel('Angle of Attack [deg]')
    plt.ylim(-6,6)
    xtab=[]
    alphatab=[]
    x=np.arange(0,(casedata(N-1)[0][0]/100)+dx,dx)
    for i in range(N):  
        plt.scatter((casedata(i)[0][0]/100),alpha(i)*(180/np.pi),0.8,marker='s')
        xtab.append((casedata(i)[0][0]/100))
        alphatab.append(alpha(i)*(180/np.pi))

    from scipy.optimize import curve_fit
    alphafit=curve_fit(sinusoid,xtab,alphatab,p0=[4.,2*np.pi/2.5,0,0])
    print(alphafit)
    plt.plot(x,sinusoid(x,alphafit[0][0],alphafit[0][1],alphafit[0][2],alphafit[0][3]))

    def alpha_MSE(x,y):
        return ((y-sinusoid(x,alphafit[0][0],alphafit[0][1],alphafit[0][2],alphafit[0][3]))**2)

    Alphamean=sum(alphatab)/N
    SSRalpha=0.
    SSTalpha=0.

    for i in range(len(xtab)):
        SSRalpha=SSRalpha+alpha_MSE(xtab[i],alphatab[i])
        SSTalpha=SSTalpha+(alphatab[i]-Alphamean)**2

    alphaRsqd=1-(SSRalpha)/(SSTalpha)
    plt.legend([('Function fit R-squared=',round(alphaRsqd,10))],prop={'size':6},loc='upper right')

    print('Angle of attack fit curve')
    print('Alpha= ',round(alphafit[0][0],3),'sin(',round(alphafit[0][1],3),'t  ',round(alphafit[0][2],3),') +',round(alphafit[0][3],3))
    print('R-squared value: ',round(alphaRsqd,6))


    print('plotting alpha function...')

    plt.show()

    




