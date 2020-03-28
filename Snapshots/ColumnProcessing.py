import numpy as np


def readsnapshotcoordinates(lines, snapshotnumber):

    Snapshots = []
    Data = []
    Value = []
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



                Value.append([x,y,z])
                Data.append(Value)
                i = i + 1
    return xx,yy,zz

#Function: Datamakecolumn
#Input: x [array], y[array]
#Output: xcols [array], ycols [array]
# Takes snapshot x, y data and groups them per markers column and outputs x and y coordinates of points in  each column

def datamakecolumn(x,y, columnlengththreshold):

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
        if round(np.sum(xcurrentcol)) not in xcolsum and len(xcurrentcol) >= columnlengththreshold:
            xcolsum.append(round(np.sum(xcurrentcol)))
            xcols.append(xcurrentcol)
            ycols.append(ycurrentcol)
    return xcols , ycols


def columnstdfilter(x,y):
    xfinalcols = []
    yfinalcols = []
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

def columnaverage(x,y):

    xmean = []
    ymean = []
    for i in range(len(x)):
        xaveragei = np.average(x[i])
        yaveragei = np.average(y[i])
        xmean.append(xaveragei)
        ymean.append(yaveragei)
    return xmean, ymean

def changeorigin(x,y,x0,y0):

    xtrue = []
    ytrue =[]
    xmin = np.amin(x)
    ymin = np.amin(y)
    xdiff = (x0-xmin)
    ydiff = (y0-ymin)

    for i in range(len(x)):
        xtruei = x[i] + xdiff
        ytruei = y[i] + ydiff
    return xtrue, ytrue

