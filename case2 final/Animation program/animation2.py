import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

c=400
xstart=-20
xstop=420
dt=0.003
R1=c*0.3
R2=(0.75-0.3)*c
R3=(1-0.75)*c
tstart=0
tstop=30
t = np.arange(tstart, tstop, dt)
tstar=np.arange(tstart, tstop, 0.01)

fig=plt.figure()
plt.title('Chord line reconstruction Case 2')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.xlim(xstart,xstop)
plt.ylim(-100,100)

def alpha(t):
    return 3.554*np.sin((2.463)*t-0.044)-0.554

def delta(t):
    return -7.056*np.sin((2.463)*t+0.021)+0.03

RP=[0.3*c,0]
plt.scatter(RP[0],RP[1],c='r')
LE, = plt.plot([RP[0]-R1], [-R1*np.sin(alpha(0)*np.pi/180)],'ro')
H,=plt.plot([RP[0]+R2],[R2*np.sin(alpha(0)*np.pi/180)],'ro')
TE,=plt.plot([400],[R3*np.sin(delta(0)*np.pi/180)],'ro')
mainchord,=plt.plot([],[],'--',c='r')
flapchord,=plt.plot([],[],'--',c='r')

def animate1(i):
    LE.set_data(RP[0]-R1*np.cos(np.pi*alpha(i)/180), -R1*np.sin(np.pi*alpha(i)/180))
    return LE,

def animate2(i):
    H.set_data(RP[0]+R2*np.cos(np.pi*alpha(i)/180), R2*np.sin(np.pi*alpha(i)/180))
    return H,

def animate3(i):
    TE.set_data(RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180),
                R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180))
    return TE,

def animate4(i):
    mainchord.set_data([RP[0]-R1*np.cos(np.pi*alpha(i)/180),RP[0]+R2*np.cos(np.pi*alpha(i)/180)],
                    [-R1*np.sin(np.pi*alpha(i)/180),R2*np.sin(np.pi*alpha(i)/180)])
    return mainchord,

def animate5(i):
    flapchord.set_data([RP[0]+R2*np.cos(np.pi*alpha(i)/180),RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180)],
                    [R2*np.sin(np.pi*alpha(i)/180),R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180)])
    return flapchord,


plot1,=plt.plot([],[],'b')
plot2,=plt.plot([],[],'b')
plot3,=plt.plot([],[],'b')
plot4,=plt.plot([],[],'b')

ds=120
x1=np.arange(25-ds,300.01-ds,0.1)
x2=np.arange(0-ds,2.51-ds,0.1)
x3=np.arange(2.5-ds,25.01-ds,0.1)

def A(t):
    return [[np.cos(alpha(t)*np.pi/180),-np.sin(alpha(t)*np.pi/180)],
            [np.sin(alpha(t)*np.pi/180),np.cos(alpha(t)*np.pi/180)]]

def g1(x):   #upper surface [25,300]
    xs=x+ds
    return -0.00000000000011617868*(xs**6) + 0.00000000016809322217*(xs**5) - 0.00000009926028837178*(xs**4) + 0.00003125813681931560*(xs**3) - 0.00601791908908675000*xs*xs +0.61905229002615000000*xs + 11.0815436954340

def vec1(x):
    return [x,g1(x)]

def transvec1(x,t):
    return np.dot(A(t),vec1(x))

def animate11(i):
    plot1.set_data(transvec1(x1,i)[0]+ds,transvec1(x1,i)[1])
    return plot1,

def animateflap(i):
    plot4.set_data([transvec1(300-120,i)[0]+ds,RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180)],
                    [transvec1(300-120,i)[1],R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180)])
    return plot4,

def g2(x):   #upper surface [0,2.5]
    xs=x+ds
    return  -0.0000888358731927497*(xs**6) + 0.0039694500932228*(xs**5) - 0.0686231864583533*(xs**4) + 0.580819579621675*(xs**3) - 2.55192552342487*xs*xs + 6.74012263900659*xs + 0.607867443369287

def vec2(x):
    return [x,g2(x)]

def transvec2(x,t):
    return np.dot(A(t),vec2(x))

def animate12(i):
    plot2.set_data(transvec2(x2,i)[0]+ds,transvec2(x2,i)[1])
    return plot2,

def g3(x):   #upper surface [2.5,25]
    xs=x+ds
    return 0.00000333051570150511*(xs**5) - 0.00027349273810982400*(xs**4) + 0.00901406935798377000*(xs**3) - 0.16073316816651200000*xs*xs + 2.14684493394407000000*xs + 3.67851944892375000000

def vec3(x):
    return [x,g3(x)]

def transvec3(x,t):
    return np.dot(A(t),vec3(x))

def animate13(i):
    plot3.set_data(transvec3(x3,i)[0]+ds,transvec3(x3,i)[1])
    return plot3,
    
Animation1 = animation.FuncAnimation(fig, animate1, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation2= animation.FuncAnimation(fig, animate2, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation3= animation.FuncAnimation(fig, animate3, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation4= animation.FuncAnimation(fig, animate4, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation5= animation.FuncAnimation(fig, animate5, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation11 = animation.FuncAnimation(fig, animate11, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation12 = animation.FuncAnimation(fig, animate12, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation13 = animation.FuncAnimation(fig, animate13, frames=np.arange(tstart, tstop,dt*10),interval=20)
Animation14= animation.FuncAnimation(fig, animateflap, frames=np.arange(tstart, tstop,dt*10),interval=20)
plt.show()


