import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

i = 0
n = -1
rawData = open(r"C:\Users\thoma\OneDrive\Bureaublad\Python\Project\Data Analysis\AE2223-I_Project_Data\AE2223-I_Project_Data\Case0","r")
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
        #print(n)
    if len(columns) == 13 and n == 2 :
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

n = -1
zpoints = []
zpointspos = []
xpoints = []
xcol = [[]]
marginx = 10
marginy = 3

for part in zz:
    n += 1
    if part > 820 and part < 860:
        zpoints.append(part)
        zpointspos.append(n)

for l in range(len(xx)):
    if l in zpointspos:
        xpoints.append(xx[l])

lengthx = len(xpoints)
xcol = [[]]

for n in range(lengthx):
    xcol.append([])

for l in range(len(xx)):
    position = xx[l]
    for n in range(len(xpoints)):
        xpoint = xpoints[n]
        if position <= xpoint + marginx and position >= xpoint - marginx:
            xcol[n].append(position)


averagessx = []
for n in range(len(xcol) - 1):
    summ = 0
    for i in range(len(xcol[n])):
        summ += xcol[n][i]
    avg = summ/(len(xcol[n]))
    averagessx.append(avg)
print(averagessx)



ypoints = []
ycol = [[]]

for l in range(len(yy)):
    if l in zpointspos:
        ypoints.append(yy[l])

lengthy = len(ypoints)
ycol = [[]]

for n in range(lengthy):
    ycol.append([])

for l in range(len(yy)):
    position = yy[l]
    for n in range(len(ypoints)):
        ypoint = ypoints[n]
        if position <= ypoint + marginy and position >= ypoint - marginy:
            ycol[n].append(position)


averagessy = []
for n in range(len(ycol) - 1):
    summ = 0
    for i in range(len(ycol[n])):
        summ += ycol[n][i]
    avg = summ/(len(ycol[n]))
    averagessy.append(avg)
print(averagessy)

plt.scatter(averagessx, averagessy)
plt.show()
        

plt.scatter(xx, yy)

plt.show()




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xx, yy, zz)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()


