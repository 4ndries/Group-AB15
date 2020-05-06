#Description
'''
So how this program will be described where the titles in Red with a'#' in frount will
represet the name of a "Block" of code and green text will explain what is happing in that block.
And hen nessissyr I will add comment tot he right of the line to explane what is going on in that line in particular

Note: Ignore the red text with 3 '#' those are there just to time how fast is the code
'''

#imports
''' Not too much to say here'''
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random                                                   
###import time 
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def Same_track_color_plot(List_of_combined_trackIDs):
    ###t = time.time()
    #Collect data
    '''here the text file that is going to be analyze, is read'''
    i = 0
    rawData = open("Case1.dat","r")
    lines = rawData.readlines()
    rawData.close()
    
    #Bounderys
    '''here we set what lines are we going to be analyze from the file'''
    start = 0
    end = 200000
    
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
    
    #Lable track IDs
    '''Now I willl be adding a small lable to the graph to mark each track ID'''
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


#Same_track_color_plot([[0, 70, 112, 153, 189, 235, 300, 312, 366, 414, 458, 501, 523, 565, 583, 648, 707, 748, 778, 801], [1, 60, 117, 181, 210, 372, 418, 470, 525, 587, 632, 700, 743, 785], [2, 68, 127, 180, 209, 255, 340, 404, 469, 505, 554, 640, 731], [3, 104, 170, 231, 310, 385, 401, 461, 514, 584, 649, 695, 726, 786], [4, 82, 164, 238, 270, 328, 377, 419, 550, 573, 650, 674, 711, 750], [5, 175, 243, 273, 323, 446, 481, 517, 561, 576, 595, 610, 663, 691, 762, 823], [6, 50, 154, 206, 269, 343, 374, 413, 449, 480, 521, 539, 563, 646, 672, 696, 721, 763, 815], [7, 55, 93, 143, 182, 225, 289, 329, 454, 502, 562, 671, 752, 806, 837], [8, 83, 222, 274, 284, 307, 442, 475, 533, 582, 616, 658, 706, 797], [8, 274, 313, 351, 442, 533, 616, 706], [8, 313, 442, 582, 706], [8, 351, 475, 616, 797], [9, 45, 124, 146, 218, 264, 311, 337, 392, 408, 463, 511, 556, 574, 722, 825], [10, 64, 155, 177, 196, 253, 306, 356, 393, 436, 545, 594, 638, 664, 716, 749, 839], [11, 57, 84, 149, 207, 230, 290, 334, 362, 394, 437, 476, 507, 547, 593, 651, 698, 792], [12, 65, 169, 205, 242, 330, 375, 412, 445, 509, 524, 557, 604, 654, 703, 779], [13, 54, 78, 150, 226, 275, 296, 359, 387, 465, 493, 571, 614, 686, 730, 767], [14, 66, 88, 129, 161, 200, 251, 364, 447, 503, 529, 585, 659, 740, 818], [15, 101, 160, 183, 227, 276, 317, 400, 427, 515, 623, 647, 702, 733, 770, 812], [16, 51, 97, 137, 184, 223, 324, 347, 370, 428, 468, 519, 526, 586, 617, 666, 794], [17, 89, 118, 249, 295, 339, 396, 429, 485, 564, 608, 693, 744, 793], [18, 46, 114, 139, 219, 268, 331, 384, 432, 500, 566, 589, 612, 680, 747, 820], [19, 79, 110, 211, 293, 332, 426, 478, 543, 675, 720, 777, 804, 828], [20, 73, 116, 151, 199, 266, 336, 438, 490, 541, 600, 629, 687, 725, 788, 813], [21, 67, 90, 185, 233, 282, 342, 430, 494, 546, 570, 598, 668, 755], [22, 107, 135, 178, 228, 302, 355, 399, 422, 460, 491, 552, 592, 636, 783, 833], [23, 59, 100, 132, 147, 163, 190, 237, 308, 341, 407, 443, 530, 567, 601, 692, 715, 782, 805, 826], [24, 85, 123, 152, 197, 353, 388, 434, 450, 477, 492, 512, 560, 591, 656, 681, 708, 746, 773, 817, 830], [25, 69, 99, 131, 168, 202, 257, 305, 358, 398, 435, 479, 537, 599, 620, 657, 766, 810, 834], [26, 48, 91, 158, 187, 241, 271, 297, 320, 350, 389, 444, 466, 536, 578, 621, 652, 738, 774, 831], [27, 53, 92, 133, 174, 213, 262, 299, 321, 354, 411, 456, 487, 553, 653, 678, 697, 734, 798, 829], [28, 74, 106, 134, 188, 234, 272, 292, 338, 395, 482, 534, 577, 611, 627, 665, 710, 768], [29, 119, 144, 186, 246, 288, 348, 380, 486, 513, 527, 633, 758, 822, 835], [30, 56, 145, 191, 247, 322, 360, 403, 431, 488, 580, 634, 662, 719, 735, 771, 811], [31, 75, 108, 128, 176, 215, 263, 301, 319, 365, 402, 471, 679, 704, 736, 757, 802, 821], [32, 113, 162, 195, 239, 304, 349, 391, 424, 451, 497, 542, 579, 622, 705], [33, 80, 148, 216, 278, 344, 379, 416, 462, 528, 603, 684, 732], [34, 61, 86, 102, 130, 159, 217, 279, 314, 361, 417, 455, 498, 544, 596, 639, 689, 814], [35, 77, 105, 165, 193, 265, 363, 441, 538, 597, 644, 661, 685, 724, 769, 809], [36, 103, 157, 198, 250, 298, 318, 378, 425, 448, 516, 575, 624, 683, 723, 753, 807, 841], [37, 76, 111, 236, 303, 357, 386, 440, 496, 568, 609, 643, 682, 712], [38, 121, 214, 252, 327, 371, 433, 504, 555, 607, 631, 669, 709, 836], [39, 96, 126, 171, 204, 221, 248, 316, 367, 381, 457, 483, 531, 572, 641, 690, 729], [40, 156, 232, 352, 415, 423, 452, 569, 615, 701, 742, 832], [41, 115, 141, 172, 224, 277, 325, 397, 421, 453, 484, 518, 559, 618, 714, 754, 824], [42, 120, 173, 254, 294, 409, 474, 510, 548, 605, 642, 677, 694, 737, 784], [43, 95, 166, 208, 260, 345, 464, 508, 602, 613, 688, 727, 751, 803, 840], [44, 87, 125, 167, 212, 261, 280, 291, 333, 369, 410, 459, 499, 549, 588, 628, 670, 761], [47, 72, 109, 203, 267, 335, 373, 405, 522, 551, 635, 667, 780], [49, 63, 122, 240, 346, 390, 439, 520, 637, 673, 728, 756, 787], [52, 98, 136, 192, 220, 309, 376, 406, 420, 467, 495, 558, 625, 660, 717, 795, 816, 838], [58, 94, 142, 194, 285, 368, 472, 535, 590, 606, 630, 655, 676, 699, 741, 772, 808], [62, 81, 138, 179, 229, 256, 382, 473, 506, 532, 581, 626, 718, 799, 827], [71, 140, 201, 286, 326, 383, 489, 540, 619, 645, 713, 764, 819], [83, 274, 351, 533, 706], [83, 313, 475, 797], [83, 351, 582], [222, 313, 533], [222, 351, 616], [245, 315], [351, 658], [739, 800]])

