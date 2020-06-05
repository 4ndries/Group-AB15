#importing modules
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from datetime import datetime
import csv
import time
#importing functions
from Combination_and_filter_function import trackid_combination
from Combination_and_filter_function import filtering
from Table_to_CSV_converter_function import used_tracks
from Table_to_CSV_converter_function import csv_export
from Plotter_function import Same_track_color_plot
from presence import ID_presence

#=================================================================
# DISCLAIMER
#
# This code runs rather slowly for Case 1 and Case 2 and you 
# should expect about 1:30 hours until it is finished.
# The programs firstly combines the trackID that form the same
# path. Afterwards, the short paths, the outliers, are removed.
# The filtered data is visualized and then exported as a csv file.            
# 
#=================================================================

#input
Case_Number = 1
x_factor = 36
y_factor = 36
z_factor = 20
Number_of_Points_to_plot = 1000000
Filter_Treshold = 1000


#opening the boolean array and the x,y,z-arrays for chosen case number
boolean_array = np.load('Case'+str(Case_Number)+'-boolean.npy')
x_position_array = np.load('Case'+str(Case_Number)+'-X.npy')
y_position_array = np.load('Case'+str(Case_Number)+'-Y.npy')
z_position_array = np.load('Case'+str(Case_Number)+'-Z.npy')
(snaps,tracks) = np.shape(boolean_array)

#combining the track ID's
print('start combining')
track_together_table = trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks,x_factor,y_factor,z_factor,ID_presence)
print('combining done')
#filter outliers
print('start filtering')
filtered_track_together_table = filtering(boolean_array,track_together_table,Filter_Treshold)
print('filtering done')
#convert filtered table into CSV file
print('start converting')
used_tracks_lst = used_tracks(filtered_track_together_table)
csv_export(used_tracks_lst,Case_Number,snaps,boolean_array,x_position_array,y_position_array,z_position_array)
print('converting done')

#plotting the filtered data
print('start plotting')
Same_track_color_plot(filtered_track_together_table,Number_of_Points_to_plot,Case_Number)
print('plotting done')
