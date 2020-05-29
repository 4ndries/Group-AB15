def trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks,x_factor,y_factor,z_factor,ID_presence):
    #first block is used to make a useful table for the remaining part of the code
    #The table is a list of lists
    #Every list consist of three elements
    #First element is the track ID number
    #Second element contains the x,y,z coordinates of the first element of the track ID
    #Third element contains the x,y,z coordinates of the last element of the track ID.
    table_i_need = []
    for i in range(tracks): #tracks is the amount of track ID's present in a case
        present = ID_presence(boolean_array,i)
        first = present[0]
        last = present[-1]
        row_i_need = [[i],[x_position_array[first][i],y_position_array[first][i],z_position_array[first][i]],[x_position_array[last][i],y_position_array[last][i],z_position_array[last][i]]]
        table_i_need.append(row_i_need)
        

    track_together_table = []
    counter = 0                                     #Use counters to break the loop and start the loop again
    second_counter = 0                              #when two track ID's are combined,
    while counter == second_counter:
        for i in range(len(table_i_need)):          #Double for-loop to be able to select two different track ID's
            find = False
            for j in range(len(table_i_need)):
                x = table_i_need[j][1][0]           #Define parameters for the ellipsoid
                x0 = table_i_need[i][2][0]
                y = table_i_need[j][1][1]
                y0 = table_i_need[i][2][1]
                z = table_i_need[j][1][2]           #LINE BELOW THESE COMMENTS: Check if the first element of the j-th track ID is in
                z0 =table_i_need[i][2][2]           #the ellipsoid around the last element of the i-th track ID
                #of course j can't be equal as i, because then you combine the same track ID's
                #j should be bigger than i because track ID's start counting from 0.
                if i != j and j > i and (x-x0)*(x-x0)/x_factor + (y-y0)*(y-y0)/y_factor + (z-z0)*(z-z0)/z_factor < 1:
                    table_i_need[i][0].extend(table_i_need[j][0])  #For example: track ID 4 and 55 are combined.  First entry of the row in table_i_need becomes [1,55] instead of [1]
                    table_i_need[i][2] = table_i_need[j][2]        #last element of track ID 4 in the table is replaced by last element of track ID 55 
                    table_i_need.pop(j)                            #Track ID 55 is removed from the table
                    counter = counter + 1                           
                    find = True
                    break                   #these 4 lines are used to start the for loop again, because the table got a new length
            if find == True:
                break
        second_counter = second_counter + 1
    #now make a new table from the first entries of the rows in the table_i_need table.   
    track_together_table = []
    for i in range(len(table_i_need)):
        track_together_row = table_i_need[i][0]
        track_together_table.append(track_together_row)
    return track_together_table         #returns a list of lists, every list is a path of track ID's

#Here the program determines the length in snapshot of the combined track ID's lists.
def filtering(boolean_array,track_together_table,Filter_Treshold):
    outliers = []
    for pair in track_together_table:           #For-loop for every combined track ID list
        points = 0
        for i in pair:
            points = points + sum(boolean_array[:,i])   #Boolean_array[:,i] is the amount of snapshots where trackID i appears. This for-loop sums all snapshot counters of all track ID's that were combined.
        
        if points <= Filter_Treshold:   #If the length of a combined track ID is lower than the Filter_Treshold than it is appended to an outlier list
            outliers.append(pair)       
    for pair in outliers:               #all combined track ID's in the outlier list are removed from the original combined track ID table.
        track_together_table.remove(pair)
    return track_together_table

