import numpy as np
import math



#Function: readSnapShotCoordinates (Tweak to original code)
#Input: lines [array of strings], snapshotnumber [int]
#Output: xx, yy, zz [array]
#Takes the lines of a data file and records the coordinates of the snapshot specified
def readsnapshotcoordinates(lines, snapshotnumber):

    xx = []
    yy = []
    zz = []

    i = 0
    n = -1

    for line in lines:
            columns = line.split(" ")
            if "ZONE T" in line:
                n += 1
            if len(columns) == 13 and n == snapshotnumber:
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
                i = i + 1
    return xx,yy,zz

#Function: Datamakecolumn
#Input: x [array] len(n), y[array] len(n)
#Output: xcols [array] len(m), ycols [array] len(m) where m < n
#Takes snapshot x, y data and groups them per markers column and outputs x and y coordinates of points in each column
def datamakecolumn(x, y, columnlengththreshold, xerror=10, yerror=10):

    xcols = []
    ycols = []
    xcolsum =[]
    for i in range(len(x)):
        xcurrentcol = [x[i]]
        ycurrentcol =[y[i]]

        for j in range(len(x)):
            if abs(x[i]-x[j])**2 <= xerror**2 and abs(y[i]-y[j])**2 <= yerror**2  and j != i:
                xcurrentcol.append(x[j])
                ycurrentcol.append(y[j])
        if round(np.sum(xcurrentcol)) not in xcolsum and len(xcurrentcol) >= columnlengththreshold:
            xcolsum.append(round(np.sum(xcurrentcol)))
            xcols.append(xcurrentcol)
            ycols.append(ycurrentcol)
    return xcols , ycols

#Function: ColumnStdFilter
#Input: x, y [array] len(n)
#Output: xfinalcols, yfinalcols [array] len(n)
#Takes column values and filters extremes using standard deviation
def columnstdfilter(x,y,z,sigma=3):
    xfinalcols = []
    yfinalcols = []
    zfinalcols = []
    for i in range(len(x)):
        xcurrentfinalcols = []
        ycurrentfinalcols = []
        zcurrentfinalcols = []
        sdx = np.std(x[i])
        sdy = np.std(y[i])
        sdz = np.std(z[i])
        xmean = np.average(x[i])
        ymean = np.average(y[i])
        zmean = np.average(z[i])
        for j in range(len(x[i])):

            if  abs(x[i][j] - xmean)**2 <= (sigma*sdx)**2 and abs(y[i][j]-ymean)**2 <= (sigma*sdy)**2 and abs(z[i][j]-zmean)**2 <= (sigma*sdz)**2:
                xcurrentfinalcols.append(x[i][j])
                ycurrentfinalcols.append(y[i][j])
                zcurrentfinalcols.append(z[i][j])

        zfinalcols.append(xcurrentfinalcols)
        yfinalcols.append(ycurrentfinalcols)
        zfinalcols.append(zcurrentfinalcols)
    return xfinalcols, yfinalcols, zfinalcols

#Function: columnAverage
#Input: x,y [array] len(n)
#Output: xmean, ymean [array] len(m) where m = n = 8
#Takes column coordinates and averages for each column returns array containg coordinates
def columnaverage(x,y):

    xmean = []
    ymean = []
    for i in range(len(x)):
        xaveragei = np.average(x[i])
        yaveragei = np.average(y[i])
        xmean.append(xaveragei)
        ymean.append(yaveragei)
    return xmean, ymean

#Function: changeOrigin
#Input: x,y [array] len(n), x0,y0 [int]
#Output: xtrue, ytrue len(n)
#Takes coordinates of point with lowest y coord and shifts it to desired origin (x0,y0)
def changeorigin(x,y,x0,y0):

    xtrue = []
    ytrue =[]
    minindex = np.argmin(x)
    xmin = np.amin(x[minindex])
    ymin = np.amin(y[minindex])
    xdiff = (x0-xmin)
    ydiff = (y0-ymin)

    for i in range(len(x)):
        xtruei = x[i] + xdiff
        ytruei = y[i] + ydiff
        xtrue.append(xtruei)
        ytrue.append(ytruei)
    return xtrue, ytrue

#Function: rotatePoints
#Input: x,y [array] len(n), anglerad [int]
#Output: xrotate,yrotate [array] len(n)
#Rotates a set of point on xy plane and rotates by angle in radian
def rotatepoints(x,y,anglerad):

    R = []
    r1 = [math.cos(anglerad),-1*math.sin(anglerad)]
    r2 = [math.sin(anglerad),math.cos(anglerad)]
    R = [r1,r2]
    xrotate = []
    yrotate = []

    for i in range(len(x)):

        v = [x[i],y[i]]
        vprime = np.dot(R,v)
        xnew = vprime[0]
        ynew = vprime[1]
        xrotate.append(xnew)
        yrotate.append(ynew)

    return xrotate,yrotate
