import csv
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import readCases as rc
import matplotlib.animation as animation
plt.style.use('dark_background')
red = [205,0,0]
snapshots = []
snapind = -1
xsnapshots = []
ysnapshots = []
rowind = 0
masteri = 0
filelocation = 'Snapshots\Case2Clean.csv'

snapshots, xsnapshots, ysnapshots = rc.readComplexCases(filelocation)
airData = open(r"Snapshots\airfoil.csv" , "r")
airlines = airData.readlines()
airData.close()
airx, airy = [], []

for airline in airlines:
    columns = airline.split(",")
    xi = float(columns[0])
    yi = float(columns[1])
    airx.append(xi)
    airy.append(yi)

xchords = xsnapshots.copy()
ychords = ysnapshots.copy()
for i in range(len(xsnapshots)):
        x1 = xsnapshots[i][0]
        x2 = xsnapshots[i][-1]
        y1 = xsnapshots[i][0]
        y2 = ysnapshots[i][-1]

        slope = (y2-y1)/(x2-x1)
        intercept = y1 - slope*x1
        xchord = np.linspace(x1,x2,20)
        ychord = slope*xchord+intercept
        np.flip(xchord)
        np.flip(ychord)
        xchords[i].append(xchord)
        ychords[i].append(ychord)



fig = plt.figure()
line, = plt.plot([],[])
plt
def init():
    line.set_data([],[])
    return line,

def animate(i):
    x = xchords[i]
    y = ychords[i]
    line.set_data(x,y)
    return line,

plt.title('Case1 Movement')
plt.axis('off')
anim = animation.FuncAnimation(fig,animate,init_func=init,frames=5000,interval=20,blit=True)
plt.show()