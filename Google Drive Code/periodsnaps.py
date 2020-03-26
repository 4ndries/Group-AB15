import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statistics
import math

#Open, read and close file
casefile = open("Case1.dat", "r")
caselines = casefile.readlines()
casefile.close()


#snapcount = 0 #n is a counter for the amount of snapshot number
#linecount = 0

snapshot = [] #includes all points (x,y,z) in a single snapshot
snapshots = [] #[0] corresponds to snapshot 0, [1] to 1 etc.
timesnapshot = []

for line in caselines:
    columns = line.split(" ")
    if len(columns) == 13:
        snapshot.append([float(columns[0]),float(columns[1]),float(columns[2])])
    if "ZONE T" in line:
        snapshots.append(snapshot)
        snapshot = []
snapshots.append(snapshot)
snapshots.remove(snapshots[0])


for line in caselines:
    new_columns = line.split(" ")
    if "SOLUTIONTIME" in line:
        time = ''.join(i for i in new_columns[-1] if i.isdigit())
        new_time = time[:-8] + '.' + time[-8:-1]
        timesnapshot.append(new_time)
timesnapshot[0] = "0.0"
new_timesnapshot = [float(i) for i in timesnapshot] #The time per snapshot, [0] is the time of snapshot 0
totalnumberofsnapshots = len(timesnapshot)

#t= 0.625s
indices = [new_timesnapshot.index(i) for i in new_timesnapshot if i>0.61 and i<0.63]
print(indices)

usesnaps = []
for ind in indices:
    usesnaps.append(snapshots[ind])
xx = []
yy = []
zz = []
for snapshot in usesnaps:
    x = [] #x column of snapshot n
    y = [] #y column of snapshot n
    z = [] #z column of snapshot n
    for point in snapshot:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    xx.append(x)
    yy.append(y)
    zz.append(z)


#Plotting
for j in range(len(xx)):
    plt.scatter(xx[j], yy[j])
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Multiple lines at roughly the same position.")
plt.legend()
plt.show()

