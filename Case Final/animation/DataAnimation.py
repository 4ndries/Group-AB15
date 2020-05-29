import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

print('Select Case (1 or 2)')
CaseSelection=input()
dx=0.1
L=15.
c=400
x_c=0.75
tstart=0                                        #start of time-domain (not really important, just for plotting)
tstop=30                                        #end of time-domain (not really important, just for plotting)

INT=100
LH=18.91814314867475

fulldata=[]
with open('case'+str(CaseSelection)+'data.txt','r') as f:
    for line in f:
        splitline=line.split("\t")
        fulldata.append(splitline)


N=int(len(fulldata)/3)
print(N,'selected data snapshots')

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

def H_chord(i):
    return [H(i)[0]+LH*np.sin(alpha(i)),H(i)[1]+LH*np.cos(alpha(i))]

def LE(i):
    return [H_chord(i)[0]-(c*x_c)*np.cos(alpha(i)),H_chord(i)[1]+(c*x_c)*np.sin(alpha(i))]

def delta(i):
    return -(np.arctan((TE(i)[1]-H_chord(i)[1])/(TE(i)[0]-H_chord(i)[0]))+alpha(i))




DY=80
fig=plt.figure()
plt.subplot(221)
plt.ylim(612-DY,612+DY)
plt.xlim(-884,-446)
points,=plt.plot(x0,y0,'ro')
LEpoint,=plt.plot([-864],[612],'o',c='orange')
TEpoint,=plt.plot([-464],[612],'go')
Hpoint,=plt.plot([c*x_c],[612],'ko')
mainchord,=plt.plot([],[],'--',c='b')
flapchord,=plt.plot([],[],'--',c='b')
segment,=plt.plot([],[],c='b')
flap,=plt.plot([],[],c='b')

def DataAnimation(i):
    points.set_data(casedata(i)[1],casedata(i)[2])
    LEpoint.set_data(LE(i)[0],LE(i)[1])
    TEpoint.set_data(TE(i)[0],TE(i)[1])
    Hpoint.set_data(H_chord(i)[0],H_chord(i)[1])
    mainchord.set_data([LE(i)[0],H_chord(i)[0]],[LE(i)[1],H_chord(i)[1]])
    flapchord.set_data([TE(i)[0],H_chord(i)[0]],[TE(i)[1],H_chord(i)[1]])
    segment.set_data(np.arange(casedata(i)[1][0],H(i)[0],0.5),f(i)(np.arange(casedata(i)[1][0],H(i)[0],0.5)))
    flap.set_data([H(i)[0],TE(i)[0]],[H(i)[1],TE(i)[1]])
    
    return points, LEpoint, TEpoint, Hpoint, mainchord, flapchord, segment, flap,

plt.legend((segment,mainchord,points,TEpoint,LEpoint,Hpoint),('case'+str(CaseSelection)+' segment','chord line','case'+str(CaseSelection)+' data points','TE','LE','Hinge'),prop={"size":8},loc='upper right')

plt.title('case'+str(CaseSelection)+ ' data animation')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
Animation1=animation.FuncAnimation(fig, DataAnimation,frames=np.arange(0,int(len(fulldata)/3),3),interval=INT,repeat=False)
#________________________________________________________________________________________________________________________________________________________________
plt.subplot(222)
plt.ylim(-DY,DY)
plt.xlim(-20,420)
plt.title('case'+str(CaseSelection)+ ' reconstruction')

#INITIAL DATA

xstart=-20                                      #start of x-domain (chordwise) (not really important, just for plotting)
xstop=420                                       #end of x-domain (chordwise) (not really important, just for plotting)
dt=0.01*1.3                                         #time step that is manually selected to be make the animation as real-timed as possible
t = np.arange(tstart, tstop, dt)                #time array (used to sample rotations of the airfoil at a given time

c=400                                           #total chord length

x_c_RP=0.3                                     #chordwise location of the rotation point (RP) (assumed from case2 data)
x_c_F=0.75                                      #chordwise location of flap hinge location (H)

#plotting stuff, setting up a figure, axis, labels etc..



#importing angle of attack and flap angle functions obtained from the case2 analysis.

def alpharec(t):
    return 3.875*np.sin(2.463*t -0.036)+0.091


def deltarec(t):
    return -7.382*np.sin(2.463*t +0.023 ) -0.03

#rotation point will not be rotated by alpha(t) and has coordinates [x,y]:
RP=[x_c_RP*c,0]
RPplot,=plt.plot([],[],'ro')


R1=c*x_c_RP                                     #radius of rotation of LE w.r.t. RP
R2=(x_c_F-x_c_RP)*c                             #radius of rotation of H w.r.t. RP
R3=(1-x_c_F)*c                                  #radius of rotation of TE w.r.t. H

#plotting initial locations ([x],[y]) of LE,Hinge (H),TE points and chordlines at t=0 these will be animated functions that can be appended through time
LErec, = plt.plot([RP[0]-R1], [0],'o',c='orange')
Hrec,=plt.plot([RP[0]+R2],[0],'ko')
TErec,=plt.plot([c],[0],'go')

#the empty mainchord list will be appended with a dotted line between the LE and H points passing through RP
#the empty flapchord list will be appended with a dotted line between the H and TE points
mainchordrec,=plt.plot([],[],'--',c='b')
flapchordrec,=plt.plot([],[],'--',c='b')

flapUp,=plt.plot([],[],'b')
flapDwn,=plt.plot([],[],'b')

plot1,=plt.plot([],[],'b')
plot2,=plt.plot([],[],'b')
plot3,=plt.plot([],[],'b')
plot4,=plt.plot([],[],'b')
plot5,=plt.plot([],[],'b')
plot6,=plt.plot([],[],'b')

#for the airfoil skin the following polynomials are used that aproximate the airfoil geomtery on three different x-domains
#The previously constructed polynomials of the airfoil geomtery are w.r.t the origin [0,0].
#however, we want to know the polynomials as a function with origin the rotation point [0.3*c,0]
#thus we shift the polynomials 0.3*c to the left
ds=x_c_RP*c

#on the domains
x1=np.arange(25-ds,300.01-ds,2)
x2=np.arange(0-ds,2.51-ds,2)
x3=np.arange(2.5-ds,25.01-ds,2)

#which give the airfoil polynomials with origin the rotation point
def g1(x):   #upper surface initial x-domain [25,300]
    xs=x+ds
    return -0.00000000000011617868*(xs**6) + 0.00000000016809322217*(xs**5) - 0.00000009926028837178*(xs**4) + 0.00003125813681931560*(xs**3) - 0.00601791908908675000*xs*xs +0.61905229002615000000*xs + 11.0815436954340

def g2(x):   #upper surface initial x-domain [0,2.5]
    xs=x+ds
    return  -0.0000888358731927497*(xs**6) + 0.0039694500932228*(xs**5) - 0.0686231864583533*(xs**4) + 0.580819579621675*(xs**3) - 2.55192552342487*xs*xs + 6.74012263900659*xs + 0.607867443369287

def g3(x):   #upper surface initial x-domain [2.5,25]
    xs=x+ds
    return 0.00000333051570150511*(xs**5) - 0.00027349273810982400*(xs**4) + 0.00901406935798377000*(xs**3) - 0.16073316816651200000*xs*xs + 2.14684493394407000000*xs + 3.67851944892375000000

def g1L(x): #lower surface initial x-domain [25,300]
    return -g1(x)

def g2L(x):
    return -g2(x)

def g3L(x): #lower surface initial x-domain [2.5,25]
    return -g3(x)

#The dot-product between the input data vector with the roation matrix will yield the rotated vector with coordinates relative to the origin (rotation point)
def transvec(x,f,t):
    return np.dot([[np.cos(alpharec(t)*np.pi/180),-np.sin(alpharec(t)*np.pi/180)],
            [np.sin(alpharec(t)*np.pi/180),np.cos(alpharec(t)*np.pi/180)]],[x,f(x)])


def animationReconstructed(i):
    
    #CHORDLINE ANIMATION
    LErec.set_data(RP[0]-R1*np.cos(np.pi*alpharec(i)/180), R1*np.sin(np.pi*alpharec(i)/180))                                                                
    RPplot.set_data(x_c_RP*c,0) 
    Hrec.set_data(RP[0]+R2*np.cos(np.pi*alpharec(i)/180), -R2*np.sin(np.pi*alpharec(i)/180))
        
    if int(CaseSelection)==1:
        TErec.set_data(RP[0]+(R2+R3)*np.cos(np.pi*alpharec(i)/180),-(R2+R3)*np.sin(np.pi*alpharec(i)/180))
        flapDwn.set_data([transvec(R2,g1L,i)[0]+ds,RP[0]+(R2+R3)*np.cos(np.pi*alpharec(i)/180)],[-transvec(R2,g1L,i)[1],-(R2+R3)*np.sin(np.pi*alpharec(i)/180)])
        flapUp.set_data([transvec(R2,g1,i)[0]+ds,RP[0]+(R2+R3)*np.cos(np.pi*alpharec(i)/180)],[-transvec(R2,g1,i)[1],-(R2+R3)*np.sin(np.pi*alpharec(i)/180)])
        
    if int(CaseSelection)==2:
        TErec.set_data(RP[0]+R2*np.cos(np.pi*alpharec(i)/180)+R3*np.cos(np.pi*deltarec(i)/180),-R2*np.sin(np.pi*alpharec(i)/180)-R3*np.sin(np.pi*deltarec(i)/180))
        flapDwn.set_data([transvec(R2,g1L,i)[0]+ds,RP[0]+R2*np.cos(np.pi*alpharec(i)/180)+R3*np.cos(np.pi*deltarec(i)/180)],[-transvec(R2,g1L,i)[1],-R2*np.sin(np.pi*alpharec(i)/180)-R3*np.sin(np.pi*deltarec(i)/180)])
        flapUp.set_data([transvec(R2,g1,i)[0]+ds,RP[0]+R2*np.cos(np.pi*alpharec(i)/180)+R3*np.cos(np.pi*deltarec(i)/180)],[-transvec(R2,g1,i)[1],-R2*np.sin(np.pi*alpharec(i)/180)-R3*np.sin(np.pi*deltarec(i)/180)])
            
    mainchordrec.set_data([RP[0]-R1*np.cos(np.pi*alpharec(i)/180),RP[0]+R2*np.cos(np.pi*alpharec(i)/180)],
                        [R1*np.sin(np.pi*alpharec(i)/180),-R2*np.sin(np.pi*alpharec(i)/180)])
    if int(CaseSelection)==1:  
        flapchordrec.set_data([RP[0]+R2*np.cos(np.pi*alpharec(i)/180),RP[0]+(R2+R3)*np.cos(np.pi*alpharec(i)/180)],
                            [-R2*np.sin(np.pi*alpharec(i)/180),-(R2+R3)*np.sin(np.pi*alpharec(i)/180)])

    if int(CaseSelection)==2:  
        flapchordrec.set_data([RP[0]+R2*np.cos(np.pi*alpharec(i)/180),RP[0]+R2*np.cos(np.pi*alpharec(i)/180)+R3*np.cos(np.pi*deltarec(i)/180)],
                            [-R2*np.sin(np.pi*alpharec(i)/180),-R2*np.sin(np.pi*alpharec(i)/180)-R3*np.sin(np.pi*deltarec(i)/180)])

    #SKIN ANIMATION
    plot1.set_data(transvec(x1,g1,i)[0]+ds,-transvec(x1,g1,i)[1])
    plot2.set_data(transvec(x2,g2,i)[0]+ds,-transvec(x2,g2,i)[1])
    plot3.set_data(transvec(x3,g3,i)[0]+ds,-transvec(x3,g3,i)[1])
    plot4.set_data(transvec(x1,g1L,i)[0]+ds,-transvec(x1,g1L,i)[1])
    plot5.set_data(transvec(x2,g2L,i)[0]+ds,-transvec(x2,g2L,i)[1])
    plot6.set_data(transvec(x3,g3L,i)[0]+ds,-transvec(x3,g3L,i)[1])
    return LErec, Hrec, TErec, RPplot, mainchord, flapchord, plot1, plot3, flapDwn, flapUp, plot4, plot6, plot2, plot5,
plt.xlabel('x* [mm]')
plt.ylabel('y* [mm]')
plt.legend((plot1,mainchord,RPplot,TErec,LErec,Hrec),('NACA0018','chord line','rotation point','TE','LE','Hinge'),prop={"size":8},loc='upper right')

faster=3.65
Animation2=animation.FuncAnimation(fig, animationReconstructed,frames=np.arange(0,36.5,(30/N)*faster),interval=INT,repeat=False)


plt.subplot(212)
plt.title('case'+str(CaseSelection)+ ' Angle plot')


dalpha,=plt.plot([],[],'bo')
ddelta,=plt.plot([],[],'o',c='orange')


#ANIMATING RECONSTRUCTED ALPHA AND DELTA
#alpha and delta will be given new names; line and line2 respectively
line,=plt.plot([],[],lw=2,c='b')
line2,=plt.plot([],[],lw=2,c='orange')


# initialization function which will make sure the animation is continious
def init():
    # creating an empty plot/frame
    line2.set_data([], [])
    line.set_data([], [])
    dalpha.set_data([],[])
    ddelta.set_data([],[])
    return line, line2, dalpha, ddelta,

tdata=[]
alphadata=[]
deltadata=[]

DT=1
#For the animation of alpha and delta the previously computed angles must be shown to make a clear view of the constructed graphs,
#Therefore the data of alpha and delta will be appended into a list, if animated will show all computations untill the current time.
def animateangles(i):
    t=DT*i
    tdata.append(t)
    alphadata.append(alpharec(t))
    line.set_data(tdata,alphadata)
    if int(CaseSelection)==2:
        deltadata.append(deltarec(t))
    if int(CaseSelection)==1:
        deltadata.append(0)   
    line2.set_data(tdata,deltadata)    
    return line, line2,  


plt.legend((line, line2),('reconstructed alpha','reconstructed delta'),loc='upper right')
plt.xlim(0,38)
if int(CaseSelection)==1:
    plt.ylim(-5,5)
if int(CaseSelection)==2:
    plt.ylim(-9,9)
    
Animation3=animation.FuncAnimation(fig, animateangles,frames=np.arange(0,36.5,(30/N)*faster),interval=INT,repeat=False)
plt.grid()
plt.xlabel('t [s]')
plt.ylabel('angles [deg]')
plt.show()
