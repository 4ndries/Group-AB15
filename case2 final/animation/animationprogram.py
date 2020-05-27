import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#___________________________________________________________________________________________________________________________________________________________________________________________________

#IMPORTATN NOTE!!!!
#the animation only runs synchronised and smooth if the animation is run in the small window of matplotlib.
#Thus, do not extend the pop up matplotlib screen if the animation is started, only run it in the small window.




#INITIAL DATA

xstart=-20                                      #start of x-domain (chordwise) (not really important, just for plotting)
xstop=420                                       #end of x-domain (chordwise) (not really important, just for plotting)
tstart=0                                        #start of time-domain (not really important, just for plotting)
tstop=30                                        #end of time-domain (not really important, just for plotting)
dt=0.01/(2*1.2)                                 #time step that is manually selected to be make the animation as real-timed as possible
t = np.arange(tstart, tstop, dt)                #time array (used to sample rotations of the airfoil at a given time

c=400                                           #total chord length

x_c_RP=0.3                                      #chordwise location of the rotation point (RP) (assumed from case2 data)
x_c_F=0.75                                      #chordwise location of flap hinge location (H)

#plotting stuff, setting up a figure, axis, labels etc..

fig=plt.figure()
plt.subplot(212)
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.xlim(xstart,xstop)
plt.ylim(-80,80)

#importing angle of attack and flap angle functions obtained from the case2 analysis.

def alpha(t):
    return 3.875*np.sin(2.463*t -0.036)+0.091


def delta(t):
    return -7.382*np.sin(2.463*t +0.023 ) -0.03

#rotation point will not be rotated by alpha(t) and has coordinates [x,y]:
RP=[x_c_RP*c,0]
plt.scatter(RP[0],RP[1],c='r')



#__________________________________________________________________________________________________________________________________________________________________________________________________

#AIFOIL SKIN 

#for the airfoil skin the following polynomials are used that aproximate the airfoil geomtery on three different x-domains
#The previously constructed polynomials of the airfoil geomtery are w.r.t the origin [0,0].
#however, we want to know the polynomials as a function with origin the rotation point [0.3*c,0]
#thus we shift the polynomials 0.3*c to the left
ds=x_c_RP*c

#on the domains
x1=np.arange(25-ds,300.01-ds,0.1)
x2=np.arange(0-ds,2.51-ds,0.1)
x3=np.arange(2.5-ds,25.01-ds,0.1)

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

def g2L(x): #lower surface initial x-domain [0,2.5]
    return -g2(x)

def g3L(x): #lower surface initial x-domain [2.5,25]
    return -g3(x)

#the airfoil curvy geomtery will be plotted untill the flap hinge (0.75 x/c)
#for the flap movement the flap is assumed to be a linear line between the trailing edge and the skin flap hinge. 

#the data vector containing [x,y] coordinates of airfoil geometry 
#(f is the function of the airfoil g1,g2,... etc)
def vec(x,f):
    return [x,f(x)]

#note that the coordinates of the data vector are relative to the new origin [0.3c,0], then can be rotated easily by a simple rotation matrix

#rotation matrix A which rotates the input vector [x,y] around the origin (rotation point)
#imported alpha function is given in degrees, therefore a conversion to radians must be made.
def A(t):
    return [[np.cos(alpha(t)*np.pi/180),-np.sin(alpha(t)*np.pi/180)],
            [np.sin(alpha(t)*np.pi/180),np.cos(alpha(t)*np.pi/180)]]

#The dot-product between the input data vector with the roation matrix will yield the rotated vector with coordinates relative to the origin (rotation point)
def transvec(x,f,t):
    return np.dot(A(t),vec(x,f))

#The animation of the skin will be animated up to the hinge (0.75 x/c), the flap skin will be animated as a simple linear line between the hinge and the TE.
#these empty data lists will be appended with the rotated vectors of all 6 functions (upper and lower surface)
plot1,=plt.plot([],[],'b')
plot2,=plt.plot([],[],'b')
plot3,=plt.plot([],[],'b')
plot4,=plt.plot([],[],'b')
plot5,=plt.plot([],[],'b')
plot6,=plt.plot([],[],'b')
#________________________________________________________________________________________________________________________________________________________________

#CHORDLINE 

R1=c*x_c_RP                                     #radius of rotation of LE w.r.t. RP
R2=(x_c_F-x_c_RP)*c                             #radius of rotation of H w.r.t. RP
R3=(1-x_c_F)*c                                  #radius of rotation of TE w.r.t. H

#plotting initial locations ([x],[y]) of LE,Hinge (H),TE points and chordlines at t=0 these will be animated functions that can be appended through time
LE, = plt.plot([RP[0]-R1], [0],'ro')
H,=plt.plot([RP[0]+R2],[0],'ro')
TE,=plt.plot([c],[0],'ro')

#the empty mainchord list will be appended with a dotted line between the LE and H points passing through RP
#the empty flapchord list will be appended with a dotted line between the H and TE points
mainchord,=plt.plot([],[],'--',c='r')
flapchord,=plt.plot([],[],'--',c='r')


#________________________________________________________________________________________________________________________________________________________________

#FLAP

#for the animation of the flap, there will simply be a line between the skin flap hinge and the trailing edge
#for the upper flap skin flapUp and lower flap skin flapDwn
flapUp,=plt.plot([],[],'b')
flapDwn,=plt.plot([],[],'b')

#_________________________________________________________________________________________________________________________________________________________________

#ANIMATION

#in the animation all the previously constructed initial (empty) lists will be appended with time-snapshotted data as functions of alpha and delta.
#If the  animation fuction is called at t=i, it will give a simple snapshot, all these snapshots played together will yield an animation

def animationCase2(i):
    #CHORDLINE ANIMATION
    LE.set_data(RP[0]-R1*np.cos(np.pi*alpha(i)/180), -R1*np.sin(np.pi*alpha(i)/180))                                                                
    
    H.set_data(RP[0]+R2*np.cos(np.pi*alpha(i)/180), R2*np.sin(np.pi*alpha(i)/180))
    
    TE.set_data(RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180),
                R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180))
    
    mainchord.set_data([RP[0]-R1*np.cos(np.pi*alpha(i)/180),RP[0]+R2*np.cos(np.pi*alpha(i)/180)],
                    [-R1*np.sin(np.pi*alpha(i)/180),R2*np.sin(np.pi*alpha(i)/180)])
    
    flapchord.set_data([RP[0]+R2*np.cos(np.pi*alpha(i)/180),RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180)],
                    [R2*np.sin(np.pi*alpha(i)/180),R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180)])

    #SKIN ANIMATION
    plot1.set_data(transvec(x1,g1,i)[0]+ds,transvec(x1,g1,i)[1])
    plot2.set_data(transvec(x2,g2,i)[0]+ds,transvec(x2,g2,i)[1])
    plot3.set_data(transvec(x3,g3,i)[0]+ds,transvec(x3,g3,i)[1])

    plot4.set_data(transvec(x1,g1L,i)[0]+ds,transvec(x1,g1L,i)[1])
    plot5.set_data(transvec(x2,g2L,i)[0]+ds,transvec(x2,g2L,i)[1])
    plot6.set_data(transvec(x3,g3L,i)[0]+ds,transvec(x3,g3L,i)[1])



   #FLAP ANIMATION
    flapUp.set_data([transvec(R2,g1,i)[0]+ds,RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180)],
                    [transvec(R2,g1,i)[1],R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180)])

    flapDwn.set_data([transvec(R2,g1L,i)[0]+ds,RP[0]+R2*np.cos(np.pi*alpha(i)/180)+R3*np.cos(np.pi*delta(i)/180)],
                    [transvec(R2,g1L,i)[1],R2*np.sin(np.pi*alpha(i)/180)+R3*np.sin(np.pi*delta(i)/180)])

   
    return LE, H, TE, mainchord, flapchord, plot1, plot2, plot3, plot4, plot5, plot6, flapUp, flapDwn,


#for the airfoil animation to be as real-timed as possible the following parameters were eyeballed (to make the animation roughly 30seconds)
INT=1
DT=1.6*2*dt

#calling the animation of reconstructed case2.
Animation1 = animation.FuncAnimation(fig, animationCase2, frames=np.arange(0,30,DT),interval=1,blit=True,repeat=False)

#________________________________________________________________________________________________________________________________________________________

#ANIMATING ALPHA AND DELTA

#in the second subfigure, alpha and delta will be animated synchronised with the case2 animation (for cool purposes only)

#setting up the figure, etc...
plt.subplot(211)
plt.title('RECONSTRUCTION CASE2')
plt.grid()
plt.xlim(0,30)
plt.ylim(-10,10)
plt.xlabel('t [s]')
plt.ylabel('angles [deg]')

#alpha and delta will be given new names; line and line2 respectively
line,=plt.plot([],[],lw=2)
line2,=plt.plot([],[],lw=2)

# initialization function which will make sure the animation is continious
def init():
    # creating an empty plot/frame
    line2.set_data([], [])
    line.set_data([], [])
    return line, line2,


tdata=[]
alphadata=[]
deltadata=[]
dt=0.01*1.6/1.2
#For the animation of alpha and delta the previously computed angles must be shown to make a clear view of the constructed graphs,
#Therefore the data of alpha and delta will be appended into a list, if animated will show all computations untill the current time.
def animateangles(i):
    t=dt*i
    tdata.append(t)
    alphadata.append(-alpha(t))
    line.set_data(tdata,alphadata)
    deltadata.append(-delta(t))
    line2.set_data(tdata,deltadata)
    return line, line2,

plt.legend((line, line2), ('alpha', 'delta'))
AnimatedAngles= animation.FuncAnimation(fig, animateangles,init_func=init,frames=3000,interval=5,blit=True,repeat=False)
plt.show()
