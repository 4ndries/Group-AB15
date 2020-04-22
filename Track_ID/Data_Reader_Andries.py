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
end = 600



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
def Same_track_color_plot(trackID,List_of_combined_trackIDs):
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
        ax.scatter(list_x[i],list_y[i],list_z[i],color=(random.randint(0,1000)/1000,random.randint(0,10000)/10000,random.randint(0,100000)/100000), marker='.')
        
        #Labling axis and clusters
        
        plt.legend(trackID)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
    #for i in range(len(list(dict.fromkeys(trackID)))):
            #ax.text(finalDf['list_x'][i],finalDf['list_y'][i],finalDf['list_z'][i],klm['TrackID'][i]) 
            #print(i)
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

Same_track_color_plot(trackID,((0, 68, 98, 111, 129, 156, 197, 208, 250, 279), (1, 62, 89, 143, 248), (2, 142, 196, 214), (4, 74, 102, 162, 198, 237), (5, 91, 169, 298), (6, 76, 160, 220), (7, 54, 73, 92, 119, 146, 171, 200, 217, 245, 262, 292), (8, 93, 144, 235, 277), (10, 79, 126, 154, 186, 209, 236, 278), (11, 61, 81, 115, 150, 189, 252, 276), (12, 85, 122, 244), (14, 69, 90, 112, 135, 163, 173, 225, 280), (15, 78, 191, 255, 291), (16, 153, 203, 295), (17, 80, 108, 127, 206, 238, 286), (18, 64, 94, 134, 151, 181, 221, 254, 265, 273, 296), (19, 63, 95, 128), (20, 70, 83, 120, 152, 182, 215, 231, 268, 299), (21, 183), (23, 116, 159, 229), (24, 114, 176, 239, 289), (25, 118, 145), (28, 96), (29, 88), (30, 59, 100, 192, 243, 287), (31, 131, 179, 211, 242, 288), (33, 77, 106, 177, 205, 258), (36, 125, 216, 300), (37, 86, 99, 121, 168, 210, 259), (38, 110, 178, 212, 253), (39, 232), (40, 202), (41, 67, 84, 107, 147, 184, 219, 226, 241, 260, 290), (42, 82, 101, 140, 166, 190, 223, 257, 271), (43, 103, 167, 213, 267), (44, 71, 104, 185, 224, 261, 274), (45, 199, 284), (46, 87, 124, 155, 174, 207, 256, 283), (47, 139, 188), (48, 72, 109, 136, 204, 246, 263), (49, 161, 249, 275), (50, 193, 230, 282), (51, 75, 149, 201, 228), (52, 105, 158, 187, 227, 266, 294), (57, 133, 172, 233, 269), (58, 97, 164, 264), (60, 123, 148, 180, 218, 272, 293)))



plt.show()


