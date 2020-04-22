import matplotlib.pyplot as plt 
import numpy as np 
import ColumnProcessing as cp

rawData = open(r"Snapshots\Case0.dat" , "r")
lines = rawData.readlines()
rawData.close()
index = 20



xx, yy, zz = cp.readsnapshotcoordinates(lines, index)
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
zcolsfinal = []
ycolsfinal = []
averageList = []

for i in range(len(xcolsraw)):
    average = round(np.average(xcolsraw[i]))

    if average not in averageList and len(xcolsraw[i]) >= 3:
        averageList.append(average)
        xcolsfinal.append(xcolsraw[i])
        zcolsfinal.append(zcolsraw[i])
        ycolsfinal.append(ycolsraw[i])
xcolsfinal,ycolsfinal,zcolsfinal = cp.columnstdfilter(xcolsfinal,ycolsfinal,zcolsfinal)





newxx = []
newzz = []
newyy = []
for i in range(len(xcolsfinal)):
    newxx.extend(xcolsfinal[i])
    newzz.extend(zcolsfinal[i])
    newyy.extend(ycolsfinal[i])

# plt.scatter(xx,yy, label='x-y plane with y on y axis')
# plt.legend()
# plt.show()

plt.scatter(xx,yy, label='x-z plane with z on y axis')
plt.legend()
plt.show()
plt.scatter(newxx,newyy, label='z-y plane with y on y axis')
plt.legend()
plt.show()



