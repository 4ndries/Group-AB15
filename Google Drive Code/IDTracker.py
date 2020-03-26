import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

case0file = open("Case1.dat", "r")
case0lines = case0file.readlines()
case0file.close()

# for line in case0lines:
#     print(line)
x = []
y = []
z = []
trackid = str(128)

for line in case0lines:
    columns = line.split(" ")
    if len(columns) == 13 and columns[8] == trackid:
        x.append(float(columns[0]))
        y.append(float(columns[1]))
        z.append(float(columns[2]))
        
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x,y,z)

ax.set_xlabel('X [mm]')
ax.set_ylabel('Y [mm]')
ax.set_zlabel('Z [mm]')

plt.show()



