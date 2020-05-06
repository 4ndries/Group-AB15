#Description
'''
So how this program will be described where the titles in Red with a'#' in frount will
represet the name of a "Block" of code and green text will explain what is happing in that block.

Note: Ignore the red text with 3 '#' those are there just to time how fast is the code
'''
def Same_track_color_plot(List_of_combined_trackIDs,Number_of_Points_to_plot,Case_Number):
    import matplotlib.pyplot as plt
    import random
    ###t = time.time()
    #Collect data
    '''here the text file that is going to be analyze, is read'''
    i = 0
    rawData = open("Case"+str(Case_Number)+ ".dat","r")
    lines = rawData.readlines()
    rawData.close()
    
    #Bounderys
    '''here we set what lines are we going to be analyze from the file'''
    start = 0
    end = Number_of_Points_to_plot
    
    #Lists
    ''' Your standard wahy iof putting all the data into lists'''
    Data = []    
    Value = []
    list_x = []
    list_y = []
    list_z = []
    trackID = []
    C = 0
    for line in lines:
        columns = line.split(" ")
        if len(columns) == 13 and i < 2*10**6:
            
            columns = line.split(" ")
            x = columns[0].strip()
            y = columns[1].strip()
            z = columns[2].strip()
            I = columns[3].strip()
            u = columns[4].strip()
            v = columns[5].strip()
            w = columns[6].strip()
            lVl = columns[7].strip()
            trackID_ = int(columns[8].strip())
            ax = columns[9].strip()
            ay = columns[10].strip()
            az = columns[11].strip()
            lal = columns[12].strip()
            list_x.append(float(x))
            list_y.append(float(y))
            list_z.append(float(z))
            trackID.append(int(trackID_))
            Value.append([x,y,z])
            Data.append(Value)
            i = i + 1

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Cut the list to size
    '''Here the lists are being cut down to the specifications in Bounderys'''
    list_x = list_x[start:end]
    list_y = list_y[start:end]
    list_z = list_z[start:end]
    trackID = trackID[start:end]
    No_of_points = len(list_x)                          #Just a counter to know how many points are being cheack

    #Making white list
    '''Here I make a list of track IDs that should be plotted in the final graph'''
    Whitelist_IDs = []
    for group in List_of_combined_trackIDs:
            for ID in group:
                if ID not in Whitelist_IDs:
                    Whitelist_IDs.append(ID)
                    
    #Redefining track IDs
    '''Here is where I change the track ID of the data points, where I give the trackIDs that should be all together the same trackID and all the ones that should be removed a track ID of -1
    NOTE: the form of List_of_combined_trackIDs looks like [(1,2,3),(4,5,6)] meaning that trackIDs 1,2 and 3 have to be be combined into one trackID'''
    
    for i in range(len(trackID)): 
        
        if trackID[i] in Whitelist_IDs:                 #Here the track ID is checked to see if it is in the white list if not then it get the track ID of -1
        
            for group in List_of_combined_trackIDs:     #The List that contains the list of track IDs that have to be combined is sperated into groups of track IDs that should be combined. 
                
                base = -2                               #Here I define an arbitrary base number which is then replaced by first trackID of the group of trackIDs that should be combined
                
                for ID in group:                        #Here I go though a list of trackIDs that should be combined and see if they are in that list if they are then they are given the value of the base (the first trackID of the group of trackIDs that should be combined)
                    if base == -2:
                        base = ID
                    if ID == trackID[i]:
                        trackID[i] = base
        else:
            trackID[i] = -1
            C = C + 1                                   #A counter to see how many points are going to be removed 
            
    print (round((100-((C/(No_of_points))*100)),2),"% of data retained(",round(((C/(No_of_points))*100),2),"% of data taken out)")  #To print out how much data is removed
    
    
    #Plotting
    '''Here the points that should be plotted with the same color are plotted'''
    for i in range(len(trackID)):
        if trackID[i] != -1:                            #First if the point does not have to be plotted (hence has a track ID of -1)
       
            
            if i%10 == 0:                               #detrimes how many points it skips before plotting anouther point (speeds up plotting a lot with out removing all the data
                
                random.seed(trackID[i])                 #The seed of the random number generator in python will changed based on the track ID, thus track IDs with the same seed and as seen the the next step will ge the same random color
                
                ax.scatter(list_x[i],list_y[i],list_z[i],color=(random.randint(0,1000)/1000,random.randint(0,10000)/10000,random.randint(0,100000)/100000), marker='.')
                
        
         

    
        ax.set_xlabel('X axis(mm)')
        ax.set_ylabel('Y axis(mm)')
        ax.set_zlabel('Z axis(mm)')
    
    #Label track IDs
    '''So to the graph I will be adding a small lable to the trackID that it is trying to trace'''
    for i in list(dict.fromkeys(trackID)):
        if trackID[i] != -1:                            #Ofc we dont want to lable track ID -1
            counter = 0
            switch = 0
            x,y,z = 0,0,0
            while switch == 0:                          #Here I want to make sure the track ID is labled only once so it goes though the list until every unqule trackID has a mark
                counter = counter + 1
                if counter > len(trackID)-2:
                    switch = 1
                if trackID[counter] == i:
                    x = list_x[counter]
                    y = list_y[counter]
                    z = list_z[counter]
                    switch = 1
            

        ax.text(x,y,z,'%s' % (str(i)), size=10, zorder=1,  color='k')
    ###print ('Time taken',"%.3f" % (time.time()-t),'s')
    return plt.show()                                   #Finally plot the graph
