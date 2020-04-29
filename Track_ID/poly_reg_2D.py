#importing modules and functions
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


#importing files
from Track_ID_Nico_original import snap_array, ID_presence, plot_3D

#opening the data file
i = 0
rawData = open("Case0.dat","r")
lines = rawData.readlines()
lines_copy = lines
rawData.close()

#initializing list
trackID = []

#reading the data file
for line in lines:
    columns = line.split(" ")
    if len(columns) == 13 and i < 10000:
        
        columns = line.split(" ")
        trackID_ = int(columns[8].strip())
        trackID.append(int(trackID_))
        i = i + 1
        
#creating data arrays
boolean_array, x_position_array, y_position_array, z_position_array = snap_array(lines_copy, trackID)

#finding the number of snapshots and track ID's in a Case
(snaps,tracks) = np.shape(boolean_array)

#generating a new way of encapsulating data for a track ID for further processing
def track_array(track,boolean_array, x_position_array, y_position_array, z_position_array):
    """
    Function for organizing the data in a an array format col 1 = snap ,col 2 = x
    col3 = y and col4 = z
    Args:
        track(int) : number of the track ID
        boolean_array: (Snpashot,Track_ID) array that identifies whether a
                        a Track ID is present in a snapshot(1) or not(0)
        x_position_array(array) : (Snpashot,Track_ID) array whose elements are the x-coord
        y_position_array(array) : (Snpashot,Track_ID) array whose elements are the y-coord
        z_position_array(array) : (Snpashot,Track_ID) array whose elements are the z-coord
    Returns:
        ar(array) : Array with 4 columns(snapshot,x,y,z) correspondant for one track ID
    """
    x, y, z, snap = [] , [] , [] ,[]
    (rows,columns) = np.shape(boolean_array)

    for i in range(0,rows):
        if boolean_array[i,track] != 0:
            x.append(x_position_array[i,track])
            y.append(y_position_array[i,track])
            z.append(z_position_array[i,track])
            snap.append(i)
    
    ar = np.zeros((len(x),4)) #creating a zero array for a track ID with snapshots and coordinates
    ar[:,0] = snap[:]
    ar[:,1] = x[:]
    ar[:,2] = y[:]
    ar[:,3] = z[:]
    
    return ar

def regression(ar,deg=3):
    """
    Function for creating of polynomial regression of degree deg
    Args:
        deg(int) : degree of polynomial
        ar(array) : Array with 4 columns(snapshot,x,y,z) correspondant for one track ID 
    Returns:
        poly_reg_funct(function) : A one-dimensional polynomial class
    """
     
    poly_reg = np.polyfit(ar[:,1], ar[:,2], deg)
    poly_reg_funct = np.poly1d(poly_reg)
    return poly_reg_funct

def pairing(tracks,boolean_array, x_position_array, y_position_array, z_position_array):
    """
    Function for reconstructing/pairing track ID's
    Args:
        tracks(int): number of track ID's of a Case
        boolean_array: (Snpashot,Track_ID) array that identifies whether a
                        a Track ID is present in a snapshot(1) or not(0)
        x_position_array(array) : (Snpashot,Track_ID) array whose elements are the x-coord
        y_position_array(array) : (Snpashot,Track_ID) array whose elements are the y-coord
        z_position_array(array) : (Snpashot,Track_ID) array whose elements are the z-coord
    Returns:
        
    """
    """ 
    for i in range(0,tracks): #going through all track ID's
        ar0 = track_array(i,boolean_array, x_position_array, y_position_array, z_position_array)
        poly_reg_funct = regression(ar0, deg=3)
        for j in range(i+1,tracks):
            ar = track_array(j,boolean_array, x_position_array, y_position_array, z_position_array)
            if abs(ar0[-1,2]-poly_reg_funct(ar[0,1])<0.05) and abs(ar0[-1,3]-poly_reg_funct(ar[0,3])<0.05):
                if ar[-1,0] == ar0[-1,0] and abs(ar[-1,1]-ar[0,1]):
                    print([i,j])"""
    track_together_table = []
    for tr in range(0,tracks):
        ar0 = track_array(tr,boolean_array, x_position_array, y_position_array, z_position_array)
        poly_reg_funct = regression(ar0, deg=3)
        for snap in range(0,snaps):
            if boolean_array[snap,tr] == 0: #we lost the track ID in this frame, we need reconstruction #verify time coord
                for tr1 in range(tr,tracks):
                    if boolean_array[snap,tr1] != 0: #the other track ID is present and can take over
                        if (abs(y_position_array[snap-1,tr]-poly_reg_funct(x_position_array[snap,tr1]))<6): #verify y coord
                            if abs(z_position_array[snap-1,tr]-z_position_array[snap,tr1])<6:# z coord
                                if abs( x_position_array[snap-1,tr]- x_position_array[snap,tr1])<6: #verify x coordinate
                                    #print([tr,tr1])
                                    track_together_table.append([tr,tr1])
    return track_together_table                             
#pairing(tracks,boolean_array, x_position_array, y_position_array, z_position_array)
              
def plot_pairs(pairs,boolean_array, x_position_array, y_position_array, z_position_array):
    """
    Function for plotting track ID's which are paired
    Args:
        pairs(list): list of track ID pairs
        boolean_array: (Snpashot,Track_ID) array that identifies whether a
                        a Track ID is present in a snapshot(1) or not(0)
        x_position_array(array) : (Snpashot,Track_ID) array whose elements are the x-coord
        y_position_array(array) : (Snpashot,Track_ID) array whose elements are the y-coord
        z_position_array(array) : (Snpashot,Track_ID) array whose elements are the z-coord
    Returns:
        None
    """
    for i,track in enumerate(pairs):
        ar = track_array(track,boolean_array, x_position_array, y_position_array, z_position_array)
        plt.plot(ar[:,1],ar[:,2],marker = "o",label = track)
    plt.legend()    
    plt.show()
    
track_together_table =  pairing(tracks,boolean_array, x_position_array, y_position_array, z_position_array)
counter = 0
second_counter = 0
while counter == second_counter:
    for i in range(len(track_together_table)):
        find = False
        for j in range(len(track_together_table)):
            if track_together_table[i][-1] == track_together_table[j][0]:
                track_together_table[j].pop(0)
                track_together_table[i] = track_together_table[i] + track_together_table[j]
                track_together_table.remove(track_together_table[j])
                find = True
                counter = counter + 1
                break
        if find == True:
            break
    second_counter = second_counter + 1

counter = 0
second_counter = 0
while counter == second_counter:
    for i in range(len(track_together_table)):
        find = False
        for j in range(len(track_together_table)):
            if all(elem in track_together_table[i] for elem in track_together_table[j]) and i != j:
                track_together_table.pop(j)
                find = True
                counter = counter + 1
                break
        if find == True:
            break
    second_counter = second_counter + 1
print(len(track_together_table))    
pairs = track_together_table[1]    
plot_pairs(pairs,boolean_array, x_position_array, y_position_array, z_position_array)

