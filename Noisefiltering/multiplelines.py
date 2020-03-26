import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statistics
import math

#Open, read and close file
case0file = open("Case0.dat", "r")
case0lines = case0file.readlines()
case0file.close()


n = -1 #n is a counter for the amount of snapshot number

x = [] #x column of snapshot n
y = [] #y column of snapshot n
z = [] #z column of snapshot n

snapshotnr = 32 #snapshot number


#Every line is converted to a list
for line in case0lines:
    columns = line.split(" ")
    if "ZONE T" in line: #Zone T indicates the snapshot number
        n += 1
    if len(columns) == 13: #Data list can be distinguished by 13 columns
        x.append(float(columns[0]))
        y.append(float(columns[1]))
        z.append(float(columns[2]))
    if n > snapshotnr:
        break
    
#The error indicates the radius in which points are assigned to a column
error = 0.01 #[mm]
xygridpoints =[]
columnslist =[]
 
#Gathers all (x,y) for each grid point
for xgridpoint in x:
    place = x.index(xgridpoint)
    ygridpoint = y[place]

    xygridpoints.append([xgridpoint,ygridpoint])

#Checks whether grid point is within the radius of error of an initial gridpoint
for i in range(0,len(xygridpoints)-0):
    column=[]
    for gridpoint in xygridpoints:
        initgridpoint = xygridpoints[i]
        if ((initgridpoint[0]-gridpoint[0])**2+(initgridpoint[1]-gridpoint[1])**2) < error**2:
                column.append(gridpoint)
    columnslist.append(column)

#Removes duplicates from list "duplicate"
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

#Calculates the average of the values in a list
def Average(lst):
    return sum(lst) / len(lst)

def SSD(list,mean):
    for elem in list:
        sigma = math.sqrt((elem-mean)**2/(len(list)-1))
    return sigma

#Duplicates are removed
new_columnslist = Remove(columnslist)

#List of averaged coordinates is prepped
averagedcoord = []
sigmax =[]
sigmay = []
#For each column the x and y values of the coordinates are averaged and combined as a point
for col in new_columnslist:
    xlist =[]
    ylist =[]
    for xycoord in col:
        xlist.append(xycoord[0])
        ylist.append(xycoord[1])
    xavg = Average(xlist)
    yavg = Average(ylist)
    #sigmax.append(SSD(xlist,xavg))
    #sigmay.append(SSD(ylist,yavg))

    averagedcoord.append([xavg,yavg])
#print(sigmax)
#print(sigmay)
#All average points are plotted
for point in averagedcoord:
    plt.scatter(point[0],point[1])
    #plt.pause(0.01)

plt.show()



