#importing modules anf unctions
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#Notes
'''
Between 450-500 data is really bad

'''

#opening the data file
i = 0
rawData = open("Case1.dat","r")
lines = rawData.readlines()
lines_copy = lines
rawData.close()

#initializing list
trackID = []

#reading the data file
for line in lines:
    columns = line.split(" ")
    if len(columns) == 13 and i < 200000:
        
        columns = line.split(" ")
        trackID_ = int(columns[8].strip())
        trackID.append(int(trackID_))
        i = i + 1

def snap_array(lines,trackID):
    
    """
    Function for organizing the data in a SnapShot-TrackID format
    Args:
        Lines(file): case file
        track_id(list): list of all trackIDs
    Returns:
        boolean_array: (Snpashot,Track_ID) array that identifies whether a
                        a Track ID is present in a snapshot(1) or not(0)
        x_position_array(array) : Snpashot,Track_ID) array whose elements are the x-coord
        y_position_array(array) : Snpashot,Track_ID) array whose elements are the y-coord
        z_position_array(array) : Snpashot,Track_ID) array whose elements are the z-coord
    """
    
    col = max(trackID) + 1 #the max value of the Track_ID gives the number of columns of the array
    i = 0
    j = 0 #row/snapshot count
    control = 0 #becomes 1 when the snapshot is ended
    #initializing lists
    xx = []
    yy = []
    zz = []
    trackID_n = []
    boolean_array = np.zeros((1,col))
    x_position_array = np.zeros((1,col))
    y_position_array = np.zeros((1,col))
    z_position_array = np.zeros((1,col))
    
    for line in lines:
        columns = line.split(None)

        if len(columns) == 13 and i < 200000:
            columns = line.split(" ")
            x = columns[0].strip()
            y = columns[1].strip()
            z = columns[2].strip()
            trackID_ = int(columns[8].strip())
            xx.append(float(x))
            yy.append(float(y))
            zz.append(float(z))
            trackID_n.append(int(trackID_))


            i = i + 1
            control = 0
            
        elif len(columns) != 13:
            
            if control == 0:
                for count,ele in enumerate(trackID_n):   #assigning values to the elements of the arrays
                    boolean_array[j-1,ele] = 1
                    x_position_array[j-1,ele] = xx[count]
                    y_position_array[j-1,ele] = yy[count]
                    z_position_array[j-1,ele] = zz[count]
                boolean_array = np.append(boolean_array,np.zeros((1,col)),axis = 0)
                x_position_array = np.append(x_position_array,np.zeros((1,col)),axis = 0)
                y_position_array = np.append(y_position_array,np.zeros((1,col)),axis = 0)
                z_position_array = np.append(z_position_array,np.zeros((1,col)),axis = 0)
                j = j + 1

            xx = []
            yy = []
            zz = []
            trackID_n = []
            control = 1
            
    return boolean_array[0:-1], x_position_array[0:-1], y_position_array[0:-1], z_position_array[0:-1]
    
boolean_array, x_position_array, y_position_array, z_position_array = snap_array(lines_copy, trackID)
 
#verify in which snpashots appears a track_id
def ID_presence(boolean_array,ID):
    """
    Function for determining in which snapshots does a track_ID appear
    Args:
        boolean_array(array): (Snpashot,Track_ID) array that identifies whether a
                        a Track ID is present in a snapshot(1) or not(0)
        ID(int): track_ID reference number 
    Returns:
        presence(list): list containing the snapshots in which ID appears
    """
    presence = []
    rows, cols = boolean_array.shape

    for i in range(0,rows):
        if boolean_array[i,ID] == 1:
            presence.append(i) #rows stays the same as snapshots are also defined from 0,not from 1

    return presence

#print(ID_presence(boolean_array,34)) #prints the snapshots in which trackID appears



            

    









