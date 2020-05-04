import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import ColumnProcessing as cp
import random
import csv
import readCases as rc
data = open(r"Snapshots\Case2Paths.csv", 'r')
lines = data.readlines()
data.close()

nsnap = 0
xsnapshots = []
ysnapshots = []
snapshots = []
truesnapshots = []
zsnapshots = []
xsnap,ysnap,zsnap = [],[],[]
trackid = []
trackids = []
lx,ly = [],[]
for line in lines:
    columns = line.split(',')

    if 'Snapshot' in line:
        crop = columns[0]
        nsnap = re.sub("[^0-9]", "",crop)
        xsnapshots.append(xsnap)
        ysnapshots.append(ysnap)
        snapshots.append(nsnap)
        trackids.append(trackid)
        zsnapshots.append(zsnap)
        xsnap = []
        ysnap = []
        trackid = []
    elif len(columns) >= 3:
        xsnap.append(float(columns[2].strip()))
        ysnap.append(float(columns[3].strip()))
        zsnap.append(float(columns[4].strip()))
        trackid.append(float(columns[1].strip()))

del xsnapshots[0]
del ysnapshots[0]
del zsnapshots[0]
del trackids[0]
del snapshots[-1]
largest = 0
for snapi in range(len(snapshots)):

    xx = np.around(xsnapshots[snapi],2)
    yy = np.around(ysnapshots[snapi],2)
    zz = np.around(zsnapshots[snapi],2)

    zmin = 620
    zmax = 835
    error = 10
    errorsqr = error**2

    xcolsraw,ycolsraw,zcolsraw = [],[],[]
    for i in range(len(xx)):

        if  zmin <= zz[i] <= zmax:
            currentcolx = []
            currentcolz = []
            currentcoly = []
            currentcolx.append(xx[i])
            currentcolz.append(zz[i])
            currentcoly.append(yy[i])
            for j in range(len(xx)):

                if  zmin <= zz[j] <= zmax and (xx[j]-xx[i])**2 <= errorsqr and j != i:
                    currentcolx.append(xx[j])
                    currentcolz.append(zz[j])
                    currentcoly.append(yy[j])
            xcolsraw.append(currentcolx)
            zcolsraw.append(currentcolz)
            ycolsraw.append(currentcoly)
    xcolsfinal = []
    zcolsinvert = []
    ycolsfinal = []
    averageList = []
    for i in range(len(xcolsraw)):
        average = round(np.average(xcolsraw[i]))

        if average not in averageList and len(xcolsraw[i]) >= 3:
            averageList.append(average)
            xcolsfinal.append(xcolsraw[i])
            zcolsinvert.append(zcolsraw[i])
            ycolsfinal.append(ycolsraw[i])
    xcolsfinal,ycolsfinal = cp.columnstdfilter(xcolsfinal,ycolsfinal)
    xmean, ymean = cp.columnaverage(xcolsfinal, ycolsfinal)

    if 9 > len(xmean) >= 8 and 9 > len(ymean) >= 8:
        lx.append(xmean)
        ly.append(ymean)
        truesnapshots.append(snapi)

    last = round(int(snapi)/int(len(snapshots)),2)*100
    if last > largest:
        largest = last
        print('Snapshots +=1 Total: ', round(int(snapi)/int(len(snapshots)),2)*100, ' %')

for i in range(len(lx)):
    newrowx = sorted(lx[i])
    newrowy = sorted(ly[i])
    lx[i] = newrowx
    ly[i] = newrowy

f = open('Snapshots\Case2BTrackIDClean.csv', 'w')


with f:
    writer = csv.writer(f)
    for i in range(len(lx)):
        snap = np.ones(len(lx[i]))
        currentsnap = snap*int(truesnapshots[i])
        coord = [currentsnap,lx[i],ly[i]]
        writer.writerows(coord)


for i in range(10):
    rand = random.randint(0,len(lx))
    plt.scatter(lx[rand][0:5],ly[rand][0:5])
    plt.plot(lx[rand][5:],ly[rand][5:])
plt.show()

newxx,newyy = [],[]