import matplotlib.pyplot as plt 
import numpy as np 
import ColumnProcessing as cp
import csv

rawData = open(r"Snapshots\Case0.dat" , "r")
lines = rawData.readlines()
rawData.close()
index = 20
xsnap = []
ysnap = []

for masteri in range(100):

    xx, yy, zz = cp.readsnapshotcoordinates(lines, masteri)
    xx = np.around(xx,2)
    yy = np.around(yy,2)
    zz = np.around(zz,2)


    zmin = 620
    zmax = 835
    error = 10
    errorsqr = error**2

    xcolsraw = []
    zcolsraw = []
    ycolsraw = []
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

    if len(xmean) == 8 and len(ymean) == 8:
        xsnap.append(xmean)
        ysnap.append(ymean)

newxx = []
newzz = []
newyy = []
for i in range(len(xsnap)):
    newxx.extend(xsnap[i])
    newyy.extend(ysnap[i])

xsnapfinal, ysnapfinal = cp.datamakecolumn(newxx,newyy,3)
xsnapfilt, ysnapfilt = cp.columnstdfilter(xsnapfinal,ysnapfinal)
xsnapmean, ysnapmean = cp.columnaverage(xsnapfilt, ysnapfilt)
coord = []
for i in range(len(xsnapmean)):
    coordi = [xsnapmean[i],ysnapmean[i]]
    coord.append(coordi)

f = open('Snapshots\Case0Clean.csv', 'w')
with f:
    writer = csv.writer(f)
    writer.writerows(coord)

plt.scatter(xsnapmean,ysnapmean, label='x-z plane with z on y axis')
plt.legend()
plt.show()




