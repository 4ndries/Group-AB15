import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random 

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
T = True
F = False
#Options
start = 0
end = 100


Snapshot = -1 #leave as -1 for off

Scatter_plot = T
Group_same_Track_IDs = T   #<----- Quite intesive
legend = F
    
Surface_plot = F
Airfoil_geometry = F
TrackIDRes = T



#Notes
'''
Between 450-500 data is really bad

'''


#Rest
i = 0
rawData = open("Case0.dat","r")
lines = rawData.readlines()
rawData.close()



Data = []    
Value = []
xx = []
yy = []
zz = []
trackID = []
for line in lines:
    columns = line.split(" ")
    if len(columns) == 13 and i < 10000:
        
        columns = line.split(" ")
        x = columns[0].strip()
        y = columns[1].strip()
        z = columns[2].strip()
        I = columns[3].strip()
        u = columns[4].strip()
        v = columns[5].strip()
        w = columns[6].strip()
        lVl = columns[7].strip()
        trackID_ = int(columns[8].strip())
        ax = columns[9].strip()
        ay = columns[10].strip()
        az = columns[11].strip()
        lal = columns[12].strip()
        xx.append(float(x))
        yy.append(float(y))
        zz.append(float(z))
        trackID.append(int(trackID_))
        Value.append([x,y,z])
        Data.append(Value)
        i = i + 1

#Sizing
if Snapshot == -1:            #add snapshot function later
    
    xx = xx[start:end]
    yy = yy[start:end]
    zz = zz[start:end]
    trackID = trackID[start:end]

    
'''
    for i in range(
    
    Track_Number = []
    for i in range(len(xx)):
'''        
        
'''    
def Track_Combiner(x_list,y_list,z_list,Track_ID):
    #Collecting all points from the same track ID together
    ID = 0
    for i in Track ID:
        if 
'''    
    
 
            
'''
#print(Data[0][0][0])
if Scatter_plot == True:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
  #  for p in range(len(xx)):
    if Group_same_Track_IDs == True:
        for i in range(len(xx)):
           # print(random.seed(a = trackID[i], version=2))
            random.seed(trackID[i])
            ax.scatter(xx[i],yy[i],zz[i],color=(random.randint(0,1000)/1000,random.randint(0,10000)/10000,random.randint(0,100000)/100000), marker='o')
        if legend == T:
            plt.legend(trackID)
    else:
        ax.scatter(xx,yy,zz,color = (1,0,0), marker='.')
        
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
'''
def Same_track_color_plot(trackID,List_of_combined_trackIDs): #(list_x,list_y,list_z,trackID,List_of_combined_trackIDs):
    #Collect data
    i = 0
    rawData = open("Case0.dat","r")
    lines = rawData.readlines()
    rawData.close()



    Data = []    
    Value = []
    list_x = []
    list_y = []
    list_z = []
    trackID = []
    for line in lines:
        columns = line.split(" ")
        if len(columns) == 13 and i < 10000:
            
            columns = line.split(" ")
            x = columns[0].strip()
            y = columns[1].strip()
            z = columns[2].strip()
            I = columns[3].strip()
            u = columns[4].strip()
            v = columns[5].strip()
            w = columns[6].strip()
            lVl = columns[7].strip()
            trackID_ = int(columns[8].strip())
            ax = columns[9].strip()
            ay = columns[10].strip()
            az = columns[11].strip()
            lal = columns[12].strip()
            list_x.append(float(x))
            list_y.append(float(y))
            list_z.append(float(z))
            trackID.append(int(trackID_))
            Value.append([x,y,z])
            Data.append(Value)
            i = i + 1

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #
    for i in range(len(trackID)):               #trackID cheaking
        for a in List_of_combined_trackIDs:     #Group of comined trackID
            #print(a)
            base = -1
            for b in a:                         #Parts of the group of trackIDs
                if base == -1:
                    base = b
                if b == trackID[i]:
                    trackID[i] = base
    print(trackID)
        
    #Changing track ID
    for i in range(len(xx)):
        
        #same color base on track ID
        random.seed(trackID[i])
        ax.scatter(list_x[i],list_y[i],list_z[i],color=(random.randint(0,1000)/1000,random.randint(0,10000)/10000,random.randint(0,100000)/100000), marker='o')
        
        #Labling axis and clusters
        
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
    for i in range(len(list(dict.fromkeys(trackID)))):
            #ax.text(finalDf['principal component 1'][i],finalDf['principal component 2'][i],finalDf['principal component 3'][i],klm['Aircraft'][i]) 
            print(i)
    return plt.show()
    
        
#if Scatter_plot == True:
#   Same_track_color_plot(xx,yy,zz,trackID,((1,2),(3,4,5),(6,7,9,10))) 
    
    


    
#Color map
if Surface_plot == True:
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X = np.array(xx)
    Y = np.array(yy)
    Z = np.array(zz)
    Y, Z = np.meshgrid(Y, Z)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=1, antialiased=True)

    # Customize the z axis.
    '''
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
'''
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)



if Airfoil_geometry == True:
    plt.plot(xx,yy, 'b.')

plt.show()
