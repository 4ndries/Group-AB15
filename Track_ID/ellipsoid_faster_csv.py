import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from presence import ID_presence
from datetime import datetime
import csv
#from Data_Reader_Andries import Same_track_color_plot

#opening the data file
boolean_array = np.load('Case2-boolean.npy')
x_position_array = np.load('Case2-X.npy')
y_position_array = np.load('Case2-Y.npy')
z_position_array = np.load('Case2-Z.npy')
(snaps,tracks) = np.shape(boolean_array)

#combining the trackID's
"""def trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks):
    t0 = datetime.now()
    table_i_need = []
    for i in range(tracks):
        present = ID_presence(boolean_array,i)
        first = present[0]
        last = present[-1]
        row_i_need = [[i],[x_position_array[first][i],y_position_array[first][i],z_position_array[first][i]],[x_position_array[last][i],y_position_array[last][i],z_position_array[last][i]]]
        table_i_need.append(row_i_need)

    "scaling factors"
    x_factor = 20
    y_factor = 20
    z_factor = 20
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
    t1 = datetime.now()
    print("Execution time for combining is", t1-t0)
    
    return track_together_table
track_together_table = trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks)


"""
#filtering sequence of the track ID's
"""
def filtering(boolean_array,track_together_table):
    outliers = []
    for pair in track_together_table:
        points = 0
        for i in pair:
            points = points + sum(boolean_array[:,i])
        
        if points <= 900:
            outliers.append(pair)
    for pair in outliers:
        track_together_table.remove(pair)
    return track_together_table
track_together_table = np.load('Case2-Combined_nofilter_20.npy',allow_pickle=True)
track_together_table = list(track_together_table)
track_together_table = filtering(boolean_array,track_together_table)


print(len(track_together_table))
np.save('Case2-Combined_filter_20', track_together_table)"""

#CSV export of the final paths

track_together_table = np.load('Case2-Combined_filter_20.npy',allow_pickle=True)
def used_tracks(track_together_table):
    used_tracks_lst = []
    for i in track_together_table:
        for j in i:
            used_tracks_lst.append(j)
    used_tracks_lst.sort()
    return used_tracks_lst

used_tracks_lst = used_tracks(track_together_table)
#removing duplicates

def csv_export(used_tracks_lst):
    used_tracks_lst_0 = []
    for i in used_tracks_lst: 
        if i not in used_tracks_lst_0: 
            used_tracks_lst_0.append(i) 

    f = open('Case2Pathsfunct.csv', 'w')
    csv.register_dialect("spaces", delimiter=" ")

    with f:
        writer = csv.writer(f)
        for i in range(0,snaps):
            writer.writerow(("Snapshot = {} .".format(i),"Track_ID","x","y","z"))
            for j in used_tracks_lst_0:
                if boolean_array[i,j] == 1:
                    writer.writerow((None,j,x_position_array[i,j],y_position_array[i,j],z_position_array[i,j]))
    f.close()
csv_export(used_tracks_lst)
