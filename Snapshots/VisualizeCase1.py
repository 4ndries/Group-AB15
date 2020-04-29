import matplotlib.pyplot as plt 
import numpy as np 
import ColumnProcessing as cp
import csv

rawData = open(r"Snapshots\Case0.dat" , "r")
lines = rawData.readlines()
rawData.close()
lx,ly, snapshots = [],[],[]

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


index = 20
xsnap = []
ysnap = []

for masteri in range(100):

    xx, yy, zz = cp.readsnapshotcoordinates(lines, masteri)
    xx = np.around(xx,2)
    yy = np.around(yy,2)
    zz = np.around(zz,2)
    xsnap = []
    ysnap = []


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
        lx.append(xmean)
        ly.append(ymean)
        snapshots.append(masteri)

for i in range(len(lx)):
    newrowx = sorted(lx[i])
    newrowy = sorted(ly[i])
    lx[i] = newrowx
    ly[i] = newrowy
print(lx)

f = open('Snapshots\Case1Clean.csv', 'w')

with f:
    writer = csv.writer(f)
    for i in range(len(lx)):
        snap = np.ones(len(lx[i]))
        currentsnap = snap*int(i)
        void = 'Snapshot' + str(i)
        coord = [currentsnap,lx[i],ly[i]]
        rowin = [void,'x', 'y']
        writer.writerow(rowin)
        writer.writerows(coord)



# plt.scatter(newxx,newyy, label='filtered data for all snapshots in Case0')
# plt.scatter(xmean,ymean,color='r',label='average position of columns for all snapshots in Case0')
# plt.title(label='PIV Case0 filtered data and column average position')
# plt.xlabel('Position along chord x [mm]')
# plt.ylabel('Position along airfoil y axis (thickness) [mm]')
# plt.legend()
# plt.show()




