def used_tracks(track_together_table):
    used_tracks_lst = []
    for i in track_together_table:
        for j in i:
            used_tracks_lst.append(j)
    used_tracks_lst.sort()
    return used_tracks_lst

def csv_export(used_tracks_lst,Case_Number,snaps,boolean_array,x_position_array,y_position_array,z_position_array):
    import csv
    used_tracks_lst_0 = []
    for i in used_tracks_lst: 
        if i not in used_tracks_lst_0: 
            used_tracks_lst_0.append(i) 

    f = open('Case'+str(Case_Number)+'Pathsfunct.csv', 'w')
    csv.register_dialect("spaces", delimiter=" ")

    with f:
        writer = csv.writer(f)
        for i in range(0,snaps):
            writer.writerow(("Snapshot = {} .".format(i),"Track_ID","x","y","z"))
            for j in used_tracks_lst_0:
                if boolean_array[i,j] == 1:
                    writer.writerow((None,j,x_position_array[i,j],y_position_array[i,j],z_position_array[i,j]))
    f.close()

