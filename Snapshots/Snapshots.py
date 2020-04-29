import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import interp1d
from scipy import interpolate
from random import random
import ColumnProcessing as cp


xsnaps = [] #Contains average column coordinates of each snapshots
ysnaps = [] # //

rawData = open(r"Snapshots\Case0.dat" , "r")
lines = rawData.readlines()
rawData.close()

airData = open(r"Snapshots\Airfoilcoord.txt" , "r")
airlines = airData.readlines()
airData.close()

airx, airy = [], []
for airline in airlines:
    columns = airline.split(",")
    xi = float(columns[0])
    yi = float(columns[1])
    airx.append(xi)
    airy.append(yi)




#For loop runs until specificed number of snapshots
for masteri in range(100):

    #Use readSnapShotCoordinates function to get x, y, z coordinates of snapshot, see ColumnProcessing module
    xx,yy,zz = cp.readsnapshotcoordinates(lines,masteri)

    #Use dataMakeColumn function to group data within columns, see ColumnProcessing module
    xcols , ycols = cp.datamakecolumn(xx,yy,3) # Array contains list with coordinates grouped in columns

    #Use ColumnStdFilter to refine columns by taking data within certain standard deviation, see ColumnProcessing module
    xfinalcols , yfinalcols = cp.columnstdfilter(xcols,ycols) # Array contains list with refinedcoordinates grouped in columns

    #Use columnAverage function to get average coordinate of each column, see ColumnProcessing module.
    xmean, ymean = cp.columnaverage(xfinalcols, yfinalcols) #Array contains column average positions, should be 8.

    xsnaps.append(xmean) #Append current snapshot column coordinate to xsnaps
    ysnaps.append(ymean) #Append current snapshot column coordinate to ysnaps

newxx = [] #New coordinate array for all coordinate points in xsnaps and ysnaps
newyy = []

#For loops fills newxx and newyy with all coordinate points from xsnaps and ysnaps
for i in range(len(xsnaps)):
    newxx.extend(xsnaps[i])
    newyy.extend(ysnaps[i])

#Use dataMakeColumn function to group newxx and newyy in columns.
xsnapcols,ysnapcols = cp.datamakecolumn(newxx,newyy,50)

#Similar Procedure to earlier in order to end up at average position of all columns of all snapshots
xsnapfinalcols,ysnapfinalcols = cp.columnstdfilter(xsnapcols,ysnapcols,1)
xsnapmean , ysnapmean = cp.columnaverage(xsnapfinalcols,ysnapfinalcols)

#Use function changeOrigin to shift all points to origin with min at origin
xsnaptrue,ysnaptrue = cp.changeorigin(xsnapmean,ysnapmean,0,0) #Array contains shifted column coords

#Intervals for x and y axis (Visualize)
xint = np.linspace(np.amin(xsnaptrue)-5,np.amax(xsnaptrue)+20,100)
yint = np.linspace(np.amin(ysnaptrue)-5,np.amax(ysnaptrue)+5,100)
xintzero = np.zeros(len(xint))
yintzero = np.zeros(len(yint))

#Index of max y value and min y value
maxindex = np.argmax(ysnaptrue)
minindex = np.argmin(ysnaptrue)

#Get slope between max and min point
slope = (ysnaptrue[maxindex]-ysnaptrue[minindex])/(xsnaptrue[maxindex]-xsnaptrue[minindex])
intercept = ysnaptrue[minindex]-slope*xsnaptrue[minindex]

#Get angle between line and x axis
anglerad = math.tan(slope)

#Y coordinate of line that passes through max and min
yslope = xint*slope+intercept

#Use function rotatePoints to rotate points by angle between line and xaxis
xsnaprotate, ysnaprotate = cp.rotatepoints(xsnaptrue,ysnaptrue,-1*anglerad)

y2snaprotate = [] #Array containing reflection around x axis of points

#Reflection of ysnaprotate around x axis
for i in range(len(ysnaprotate)):
    y2snaprotatei = -1*ysnaprotate[i]
    y2snaprotate.append(y2snaprotatei)

#Shift column averages to line up with airfoil
shiftxsnap ,shiftysnap = cp.changeorigin(xsnaptrue,ysnaptrue,140,-35.4205) #Last two arguments of function should be position of first marker on airfoil
shifty2snap = [] # Array containing mirrored points (x-axis reflection)

#Appends reflected points to shifty2snap
for i in range(len(shiftysnap)):
    shifty2snapi = -1*shiftysnap[i]
    shifty2snap.append(shifty2snapi)

print(xsnapmean,ysnapmean)

# #Create intervals to plot x and y axis
# xairint = np.linspace(-10,450,1000)
# yairint = np.linspace(-100,100,1000)
# xairintzero = np.zeros(len(xairint))
# yairintzero = np.zeros(len(yairint))

#Plot airfoil c=400mm with column position superposed
plt.ylim(-100,100) #Set y axis range (for scaling)
plt.scatter(airx,airy,label='airfoil c=400m') #Airfoil data
plt.plot(xairint,yairintzero) # x axis
plt.plot(xairintzero,yairint) # y axis
plt.scatter(shiftxsnap,shiftysnap) #column position shifted to fit on airfoil
plt.scatter(shiftxsnap,shifty2snap) #Mirror of column position
plt.legend()
plt.show()

# #Few interesting plots
# fig, axs = plt.subplots(2, 2)
# axs[0, 0].scatter(xx, yy, s=10)
# axs[0, 0].set_title('Single Snapshot Coordinate Data')
# axs[0, 1].scatter(xsnaps[0], ysnaps[0],s=10)
# axs[0, 1].set_title('Single Snapshot Refined Column Position')
# axs[1, 0].scatter(newxx, newyy, s=10, marker='x')
# axs[1, 0].set_title('Refined Column Position of All Snapshots')
# axs[1, 1].scatter(xsnapmean, ysnapmean,s=10)
# axs[1, 1].set_title('Final Refined Column Position based on all snapshots')
# plt.show()

# fig2, axs2 = plt.subplots(2, 2)
# axs2[0, 0].scatter(xsnaptrue, ysnaptrue, c='red')
# axs2[0, 0].plot(xint,yslope)
# axs2[0, 0].plot(xint,yintzero)
# axs2[0, 0].plot(xintzero,yint)
# axs2[0, 0].set_title('Final Refined Column Position shifted at zero with approx slope')
# axs2[0, 1].scatter(xsnaprotate, ysnaprotate, c='red')
# axs2[0, 1].plot(xint,yintzero)
# axs2[0, 1].plot(xintzero,yint)
# axs2[0, 1].set_title('Same points rotated by angle b/ x axis and line')
# axs2[1, 0].scatter(xsnaprotate, ysnaprotate, c='red')
# axs2[1, 0].scatter(xsnaprotate, y2snaprotate, c='red')
# axs2[1, 0].plot(xint,yintzero)
# axs2[1, 0].plot(xintzero,yint)
# axs2[1, 0].set_title('Rotated and Reflected')
# plt.show()







