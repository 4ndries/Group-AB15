import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import interp1d
from scipy import interpolate

i = 0
n = -1
rawData = open(r"C:\Users\mateo\Documents\python\ProjectTest\Case1.dat" , "r")
lines = rawData.readlines()
rawData.close()

Snapshots = []
Data = []
Value = []
xx = []
yy = []
zz = []
xsnaps = []
ysnaps = []
nsnaps = [0,100,200,300]

for masteri in range(len(nsnaps)):

    i = 0
    n = -1
    rawData = open(r"C:\Users\mateo\Documents\python\ProjectTest\Case1.dat" , "r")
    lines = rawData.readlines()
    rawData.close()

    Snapshots = []
    Data = []
    Value = []
    xx = []
    yy = []
    zz = []

    for line in lines:
        columns = line.split(" ")
        if "ZONE T" in line:
            n += 1
        if len(columns) == 13 and n == nsnaps[masteri]:
            columns = line.split(" ")
            x = float(columns[0].strip())
            y = float(columns[1].strip())
            z = float(columns[2].strip())
            I = columns[3].strip()
            u = columns[4].strip()
            v = columns[5].strip()
            w = columns[6].strip()
            lVl = columns[7].strip()
            trackID = int(columns[8].strip())
            ax = columns[9].strip()
            ay = columns[10].strip()
            az = columns[11].strip()
            lal = columns[12].strip()


            xx.append(x)
            yy.append(y)
            zz.append(z)


            Value.append([x,y,z])
            Data.append(Value)
            i = i + 1

    #Function: Datamakecolumn
    #Input: x [array], y[array]
    #Output: xcols [array], ycols [array]
    # Takes snapshot x, y data and groups them per markers column and outputs x and y coordinates of points in  each column

    def datamakecolumn(x,y):

        xcols = []
        ycols = []
        xcolsum =[]
        for i in range(len(x)):
            xcurrentcol = [x[i]]
            ycurrentcol =[y[i]]

            for j in range(len(x)):
                if abs(x[i]-x[j])**2 + abs(y[i]-y[j])**2 <= 100  and j != i:
                    xcurrentcol.append(x[j])
                    ycurrentcol.append(y[j])
            if round(np.sum(xcurrentcol)) not in xcolsum and len(xcurrentcol) >= 3:
                xcolsum.append(round(np.sum(xcurrentcol)))
                xcols.append(xcurrentcol)
                ycols.append(ycurrentcol)
        return xcols , ycols


    xcols , ycols = datamakecolumn(xx,yy)
    xfinalcols = []
    yfinalcols = []
    xcurrentfinalcols = []
    ycurrentfinalcols = []

    def columnstdfilter(x,y):
        for i in range(len(x)):
            xcurrentfinalcols = []
            ycurrentfinalcols = []
            sd = np.std(x[i])
            xmean = np.average(x[i])
            ymean = np.average(y[i])
            for j in range(len(x[i])):

                if  abs(x[i][j] - xmean)**2 + abs(y[i][j] - ymean)**2 <= 9*sd**2:
                    xcurrentfinalcols.append(x[i][j])
                    ycurrentfinalcols.append(y[i][j])
            xfinalcols.append(xcurrentfinalcols)
            yfinalcols.append(ycurrentfinalcols)
        return xfinalcols, yfinalcols

    xfinalcols , yfinalcols = columnstdfilter(xcols,ycols)

    xmean = []
    ymean = []

    def columnaverage(x,y):
        xmean = []
        ymean = []
        for i in range(len(x)):
            xaveragei = np.average(x[i])
            yaveragei = np.average(y[i])
            xmean.append(xaveragei)
            ymean.append(yaveragei)
        return xmean, ymean

    xmean, ymean = columnaverage(xfinalcols, yfinalcols)

    xdiff = (0-np.amin(xmean))
    ydiff = (0-np.amin(ymean))

    xtrue = []
    ytrue = []
    for i in range(len(xmean)):

        xtruei = xmean[i]+xdiff
        ytruei = ymean[i]+ydiff
        xtrue.append(xtruei)
        ytrue.append(ytruei)

    xsnaps.append(xmean)
    ysnaps.append(ymean)

code = ['ro', 'bo', 'yo', 'go']
ss = [str(nsnaps[0]),str(nsnaps[1]),str(nsnaps[2]),str(nsnaps[3])]


for i in range(len(xsnaps)):

    plt.plot(xsnaps[i],ysnaps[i],code[i], label=ss[i])
    plt.legend()

plt.show()


# slope = float((np.amax(ymean)-np.amin(ymean))/(np.amax(xmean)-np.amin(xmean)))
# intercept = float(np.amin(ymean)-slope*np.amin(xmean))
# A = 1
# B = slope
# C = intercept
# D = B**2 - A**2
# E = 2*A*B
# F  = 2*A*C
# G = A**2 + B**2
# H = A**2 - B**2
# I = 2*B*C


# x2mean = []
# y2mean = []
# for i in range(len(xmean)):

#     x2meani = (0.982*xmean[i]+0.26826*ymean[i]-180.5)*0.982327
#     y2meani = (-0.982*ymean[i]+0.26826*xmean[i]+1345.7)*0.982327
#     x2mean.append(x2meani)
#     y2mean.append(y2meani)



#f2 = interp1d(xmean, ymean, kind = 'cubic')
#f1 = interp1d(x2mean,y2mean,kind='cubic')
#xplot = np.linspace(np.amin(xmean),np.amax(xmean),1000)
#yplot = f2(xplot)
#x2plot = np.linspace(np.amin(x2mean),np.amax(x2mean),1000)
#y2plot = f1(xplot)
#plt.plot(xtrue,ytrue, "ro")
#plt.plot(xnew,ynew)
#plt.plot(xplot,yplot)
#plt.plot(x2mean,y2mean,"bo")
#plt.plot(x2plot,y2plot)
#plt.plot(x2mean,y2mean,"bo")

#plt.show()
#print(slope,intercept)
#print(xtrue,ytrue)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(xx, yy, zz)

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# plt.show()



# numcol = 0
# xcols = []
# xcolsum = []
# ycols = []
# ycolsum = []
# yroundcurrent = []
# for i in range(len(xx)):
#     xcurrentcol =[]
#     ycurrentcol = []
#     xcurrentcol.append(xx[i])
#     ycurrentcol.append(yy[i])

#     for j in range(len(xx)):
#         if abs(xx[i] -xx[j]) <= 10 and j != i:
#             xcurrentcol.append(xx[j])
#             ycurrentcol.append(yy[j])


#     if round(np.sum(xcurrentcol)) not in xcolsum:
#         xcolsum.append(round(np.sum(xcurrentcol)))
#         xcols.append(xcurrentcol)
#         ycols.append(ycurrentcol)


# yfinalcols =[]
# xfinalcols = []
# for i in range(len(xcols)):
#     if len(xcols[i]) >= 3:
#         xfinalcols.append(xcols[i])
#         yfinalcols.append(ycols[i])



# xaveragearr = []
# yaveragearr = []
# for i in range(len(xfinalcols)):
#     xaveragei = np.sum(xfinalcols[i])/len(xfinalcols[i])
#     yaveragei = np.sum(yfinalcols[i])/len(yfinalcols[i])
#     xaveragearr.append(xaveragei)
#     yaveragearr.append(yaveragei)




#plt.plot(xaveragearr,yaveragearr,'ro', label = "averagex-y pos")


