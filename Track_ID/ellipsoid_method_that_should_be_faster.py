import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from Track_ID_Nico import snap_array
from Track_ID_Nico import ID_presence
from Data_Reader_Andries import Same_track_color_plot
import time
import  datetime
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
    if len(columns) == 13 and i < 300000:
        
        columns = line.split(" ")
        trackID_ = int(columns[8].strip())
        trackID.append(int(trackID_))
        i = i + 1

boolean_array, x_position_array, y_position_array, z_position_array = snap_array(lines_copy, trackID)
(snaps,tracks) = np.shape(boolean_array)
start_time = time.time()
def trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks):
    t0 = datetime.now()
    table_i_need = []
    for i in range(max(trackID)+1):
        present = ID_presence(boolean_array,i)
        first = present[0]
        last = present[-1]
        row_i_need = [[i],[x_position_array[first][i],y_position_array[first][i],z_position_array[first][i]],[x_position_array[last][i],y_position_array[last][i],z_position_array[last][i]]]
        table_i_need.append(row_i_need)

    "scaling factors"
    x_factor = 50
    y_factor = 50
    z_factor = 50
    track_together_table = []
    counter = 0
    second_counter = 0
    while counter == second_counter:
        for i in range(len(table_i_need)):
            find = False
            for j in range(len(table_i_need)):
                x = table_i_need[j][1][0]
                x0 = table_i_need[i][2][0]
                y = table_i_need[j][1][1]
                y0 = table_i_need[i][2][1]
                z = table_i_need[j][1][2]
                z0 =table_i_need[i][2][2]
                if i != j and j > i and (x-x0)*(x-x0)/x_factor + (y-y0)*(y-y0)/y_factor + (z-z0)*(z-z0)/z_factor < 1:
                    table_i_need[i][0].extend(table_i_need[j][0])
                    table_i_need[i][2] = table_i_need[j][2]
                    table_i_need.pop(j)
                    counter = counter + 1
                    find = True
                    break
            if find == True:
                break
        second_counter = second_counter + 1 
    track_together_table = []
    for i in range(len(table_i_need)):
        track_together_row = table_i_need[i][0]
        track_together_table.append(track_together_row)
    return track_together_table
track_together_table = trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks)


def filtering(boolean_array,track_together_table):
    outliers = []
    for pair in track_together_table:
        points = 0
        for i in pair:
            points = points + sum(boolean_array[:,i])
        
        if points <= 65:
            outliers.append(pair)
    for pair in outliers:
        track_together_table.remove(pair)
    return track_together_table

track_together_table = filtering(boolean_array,track_together_table)

print(track_together_table)
print("--- %s seconds ---" % (time.time() - start_time))
#Same_track_color_plot(track_together_table)


