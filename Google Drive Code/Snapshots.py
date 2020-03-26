import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

i = 0
n = -1
rawData = open(r"C:\Users\thoma\OneDrive\Bureaublad\Data Analysis\AE2223-I_Project_Data\AE2223-I_Project_Data\Case2.dat","r")
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
    if len(columns) == 13 and (n == 2000 or n==30):  
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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xx, yy, zz)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()


