def used_tracks(track_together_table):
    """
    Function for organizing the remaining Tracks ID's after filtering
    Args:
        track_together_table(list): list of all paths after filtering. its elements consist of lists which have as
                                    as elements the track ID that construct a path together
    Returns:
        used_tracks_lst(list) : list of all the Track ID that appear in a case after filtering 
    """
    used_tracks_lst = []
    for i in track_together_table:
        for j in i:
            used_tracks_lst.append(j) #we append every trackID
    used_tracks_lst.sort()            #sort them out in ascending order for better organization
    return used_tracks_lst

def csv_export(used_tracks_lst,Case_Number,snaps,boolean_array,x_position_array,y_position_array,z_position_array):
    """
    Function for exporting the results of the outlier detection in a CSV format for the noise filtering group.
    Args:
        used_tracks_lst(list) : list of all the Track ID that appear in a case after filtering
        Case_Number(int): case number
        snaps(int): number of snapshots in the case
        boolean_array: (Snpashot,Track_ID) array that identifies whether a
                        a Track ID is present in a snapshot(1) or not(0)
        x_position_array(array) : Snpashot,Track_ID) array whose elements are the x-coord
        y_position_array(array) : Snpashot,Track_ID) array whose elements are the y-coord
        z_position_array(array) : Snpashot,Track_ID) array whose elements are the z-coord
    Returns:
        
    """
    import csv
    used_tracks_lst_0 = []
    for i in used_tracks_lst: 
        if i not in used_tracks_lst_0: 
            used_tracks_lst_0.append(i) 

    f = open('Case'+str(Case_Number)+'Pathsfunct.csv', 'w') #file in which the program will write
    csv.register_dialect("spaces", delimiter=" ") #defines that the values will be delimited by a space

    with f:
        writer = csv.writer(f)      #defines that the writer function is used for writing in the f file
        for i in range(0,snaps):    #we go through every snapshot
            writer.writerow(("Snapshot = {} .".format(i),"Track_ID","x","y","z")) #header row of each snapshot
            for j in used_tracks_lst_0:
                if boolean_array[i,j] == 1:
                    writer.writerow((None,j,x_position_array[i,j],y_position_array[i,j],z_position_array[i,j]))
    f.close()

