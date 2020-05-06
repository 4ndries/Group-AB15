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

    









