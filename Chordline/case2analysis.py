import math
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors
colors=['b','olive','orange','purple','grey','black']
dx=0.1
L=15.
c=400
x_c=0.75
N=1500

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

def f_prime(x):
    return f0[1]+2*f0[2]*x+3*f0[3]*x*x

theta0=np.arctan(f_prime(H0[0]))

x0range=np.arange(x0[0],TE0[0]+dx,dx)


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

def theta(i,x):
    return f(i)[1]+2*f(i)[2]*x+3*f(i)[3]*x*x

def alpha(i):
    return theta0-np.arctan(theta(i,H0[0]))

def sinusoid(x,A,w,phi,c1):
    return A*np.sin(w*x+phi)+c1





x=np.arange(0,29+dx,dx)
plt.figure(1)
plt.subplot(211)
for i in range(N):
    plt.scatter((casedata(i)[0][0]/100),alpha(i)*(180/np.pi))

plt.plot(x,sinusoid(x,2.2,2*np.pi/2.,0,-0.6))
plt.xlabel('time [sec]')
plt.ylabel('Angle of Attack [deg]')
plt.title('Angle of Attack case 2')



LH=18.91814314867475

def H_chord(i):
    return [H(i)[0]+LH*np.sin(alpha(i)),H(i)[1]+LH*np.cos(alpha(i))]

def LE(i):
    return [H_chord(i)[0]-(c*x_c)*np.cos(alpha(i)),H_chord(i)[1]+(c*x_c)*np.sin(alpha(i))]

def delta(i):
    return -np.arctan((TE(i)[1]-H_chord(i)[1])/(TE(i)[0]-H_chord(i)[0]))



plt.subplots_adjust(hspace=0.5)
plt.subplot(212)
plt.plot(x,sinusoid(x,-4,2*np.pi/1.98,0,0))
for i in range(N):
    plt.scatter((casedata(i)[0][0]/100),delta(i)*(180/np.pi))
plt.xlabel('time [sec]')
plt.ylabel('Flap deflection angle [deg]')
plt.title('Flap deflection angle case 2')
plt.show()

plt.scatter(x0,y0,c='r')
plt.scatter(TE0[0],TE0[1],s=100,c='r')
plt.scatter(LE0[0],LE0[1],s=100,c='r')
plt.scatter(H0[0],H0[1],s=100,c='r')
plt.plot(x0range,f0(x0range),linewidth=6,c='r')
plt.plot([TE0[0],LE0[0]],[TE0[1],LE0[1]],linewidth=4,c='r')
plt.legend(['case0'])

for i in range(N):
    xrange=np.arange(casedata(i)[1][0],H(i)[0]+dx,dx)
    xlinrange=np.arange(H(i)[0],TE(i)[0]+dx,dx)
    plt.scatter(casedata(i)[1],casedata(i)[2],c='b')
    plt.scatter(TE(i)[0],TE(i)[1],s=50,c='b')
    plt.scatter(H(i)[0],H(i)[1],s=50,c='b')
    plt.scatter(H_chord(i)[0],H_chord(i)[1],s=50,c='b')
    plt.scatter(LE(i)[0],LE(i)[1],s=50,c='b')
    plt.plot([LE(i)[0],H_chord(i)[0]],[LE(i)[1],H_chord(i)[1]],'--',c='b')
    plt.plot([H_chord(i)[0],H(i)[0]],[H_chord(i)[1],H(i)[1]],'--',c='b')
    plt.plot([H_chord(i)[0],TE(i)[0]],[H_chord(i)[1],TE(i)[1]],c='b')
    plt.plot(xrange,f(i)(xrange),'--',c='b')
    plt.plot(xlinrange,flapdata(i)(xlinrange),c='b')


plt.ylim(525,675)
plt.grid()
#plt.show()


















