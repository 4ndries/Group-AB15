def trackid_combination(boolean_array,x_position_array,y_position_array,z_position_array,tracks,x_factor,y_factor,z_factor,ID_presence):
    table_i_need = []
    for i in range(tracks):
        present = ID_presence(boolean_array,i)
        first = present[0]
        last = present[-1]
        row_i_need = [[i],[x_position_array[first][i],y_position_array[first][i],z_position_array[first][i]],[x_position_array[last][i],y_position_array[last][i],z_position_array[last][i]]]
        table_i_need.append(row_i_need)

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

def filtering(boolean_array,track_together_table,Filter_Treshold):
    outliers = []
    for pair in track_together_table:
        points = 0
        for i in pair:
            points = points + sum(boolean_array[:,i])
        
        if points <= Filter_Treshold:
            outliers.append(pair)
    for pair in outliers:
        track_together_table.remove(pair)
    return track_together_table

