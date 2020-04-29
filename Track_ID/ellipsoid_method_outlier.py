import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from Track_ID_Nico_original import snap_array
from Track_ID_Nico_original import ID_presence

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

boolean_array, x_position_array, y_position_array, z_position_array = snap_array(lines_copy, trackID)
(snaps,tracks) = np.shape(boolean_array)
table_i_need = []
for i in range(max(trackID)+1):
    present = ID_presence(boolean_array,i)
    first = present[0]
    last = present[-1]
    row_i_need = [i,[x_position_array[first][i],y_position_array[first][i],z_position_array[first][i]],[x_position_array[last][i],y_position_array[last][i],z_position_array[last][i]]]
    table_i_need.append(row_i_need)

"scaling factors"
x_factor = 5
y_factor = 5
z_factor = 8
track_together_table = []
for i in range(len(table_i_need)):
    for j in range(len(table_i_need)):
        x = table_i_need[j][1][0]
        x0 = table_i_need[i][2][0]
        y = table_i_need[j][1][1]
        y0 = table_i_need[i][2][1]
        z = table_i_need[j][1][2]
        z0 =table_i_need[i][2][2]
        if i != j and j > i and (x-x0)*(x-x0)/x_factor + (y-y0)*(y-y0)/y_factor + (z-z0)*(z-z0)/z_factor < 1:
            track_together = [table_i_need[i][0],table_i_need[j][0]]
            track_together_table.append(track_together)
    
  
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
for i in range(0,tracks):
    if (sum(boolean_array[:,i]) > 80):
        track_together_table.append([i])

def filtering(boolean_array,track_together_table):
    outliers = []
    for pair in track_together_table:
        points = 0
        for i in pair:
            points = points + sum(boolean_array[:,i])
        
        if points <= 40:
            outliers.append(pair)
    for pair in outliers:
        track_together_table.remove(pair)
    return track_together_table

track_together_table = filtering(boolean_array,track_together_table)
print(len(track_together_table)) 
 
