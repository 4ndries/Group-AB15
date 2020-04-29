import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random 

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
T = True
F = False
#Options
start = 0
end = 200000


Snapshot = -1 #leave as -1 for off

Scatter_plot = T
Group_same_Track_IDs = T   #<----- Quite intesive
legend = F
    
Surface_plot = F
Airfoil_geometry = F
TrackIDRes = T



#Notes
'''
Between 450-500 data is really bad

'''


#Rest
i = 0
rawData = open("Case1.dat","r")
lines = rawData.readlines()
rawData.close()



Data = []    
Value = []
xx = []
yy = []
zz = []
trackID = []
for line in lines:
    columns = line.split(" ")
    if len(columns) == 13 and i < 10000:
        
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
        xx.append(float(x))
        yy.append(float(y))
        zz.append(float(z))
        trackID.append(int(trackID_))
        Value.append([x,y,z])
        Data.append(Value)
        i = i + 1

#Sizing
if Snapshot == -1:            #add snapshot function later
    
    xx = xx[start:end]
    yy = yy[start:end]
    zz = zz[start:end]
    trackID = trackID[start:end]

    
'''
    for i in range(
    
    Track_Number = []
    for i in range(len(xx)):
'''        
        
'''    
def Track_Combiner(x_list,y_list,z_list,Track_ID):
    #Collecting all points from the same track ID together
    ID = 0
    for i in Track ID:
        if 
'''    
    
 
            
'''
#print(Data[0][0][0])
if Scatter_plot == True:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
  #  for p in range(len(xx)):
    if Group_same_Track_IDs == True:
        for i in range(len(xx)):
           # print(random.seed(a = trackID[i], version=2))
            random.seed(trackID[i])
            ax.scatter(xx[i],yy[i],zz[i],color=(random.randint(0,1000)/1000,random.randint(0,10000)/10000,random.randint(0,100000)/100000), marker='o')
        if legend == T:
            plt.legend(trackID)
    else:
        ax.scatter(xx,yy,zz,color = (1,0,0), marker='.')
        
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
'''
def Same_track_color_plot(trackID,List_of_combined_trackIDs):
    #Collect data
    i = 0
    rawData = open("Case0.dat","r")
    lines = rawData.readlines()
    rawData.close()
    



    Data = []    
    Value = []
    list_x = []
    list_y = []
    list_z = []
    trackID = []
    for line in lines:
        columns = line.split(" ")
        if len(columns) == 13 and i < 10000:
            
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

     #Temp take this out later
    list_x = list_x[start:end]
    list_y = list_y[start:end]
    list_z = list_z[start:end]
    trackID = trackID[start:end]
   
    for i in range(len(trackID)):               #trackID cheaking
        for a in List_of_combined_trackIDs:     #Group of comined trackID
            #print(a)
            base = -1
            for b in a:                         #Parts of the group of trackIDs
                if base == -1:
                    base = b
                if b == trackID[i]:
                    trackID[i] = base
    
    
                    
   
 
    
    #Changing track ID
    for i in range(len(xx)):
        
        #same color base on track ID
        random.seed(trackID[i])
        ax.scatter(list_x[i],list_y[i],list_z[i],color=(random.randint(0,1000)/1000,random.randint(0,10000)/10000,random.randint(0,100000)/100000), marker='.')
        
        #Labling axis and clusters
         
        #plt.legend(trackID)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

    #print(list(dict.fromkeys(trackID)))
    for i in list(dict.fromkeys(trackID)):
        counter = 0
        switch = 0
        x,y,z = 0,0,0
        while switch == 0:
            #if couter 
            counter = counter + 1
            if counter > len(trackID)-2:
                switch = 1
            if trackID[counter] == i:
                x = list_x[counter]
                y = list_y[counter]
                z = list_z[counter]
                #print(trackID[counter],x,y,z,counter)   
                switch = 1
                
            
                
            #ax.text(finalDf['list_x'][i],finalDf['list_y'][i],finalDf['list_z'][i],klm['TrackID'][i])
        ax.text(x,y,z,  '%s' % (str(i)), size=20, zorder=1,  color='k')
            #print(i)
    return plt.show()
    
        
#if Scatter_plot == True:
#   Same_track_color_plot(xx,yy,zz,trackID,((1,2),(3,4,5),(6,7,9,10))) 
    
    


    
#Color map
if Surface_plot == True:
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X = np.array(xx)
    Y = np.array(yy)
    Z = np.array(zz)
    Y, Z = np.meshgrid(Y, Z)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=1, antialiased=True)

    # Customize the z axis.
    '''
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
'''
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)



if Airfoil_geometry == True:
    plt.plot(xx,yy, 'b.')

Same_track_color_plot(trackID,((0, 112, 153, 189, 235, 300, 312), (0, 300, 414, 458, 501, 523, 565, 583, 648, 707, 748, 778, 801), (1, 60, 117, 181, 210, 372, 418, 470), (1, 525, 587, 632, 700, 743, 785), (2, 469, 505, 554, 640, 731), (4, 82, 164, 238, 270, 328, 419, 550, 573, 650, 674, 711, 750), (5, 175, 243, 273, 323, 446, 481, 517, 561, 576, 595, 610, 691, 762), (6, 480, 521, 539, 563, 646, 672, 696, 721, 763, 815), (7, 502, 562, 671, 752, 806, 837), (9, 45, 124, 146, 392, 408, 463, 511, 556, 574, 825), (10, 64, 155, 177, 196), (11, 57, 84, 149, 207, 230), (11, 476, 507, 547, 593), (12, 65, 169, 205, 242, 330, 375, 412, 445), (13, 54, 78, 150, 226, 275, 296, 359, 387, 465, 493, 571, 614), (14, 66, 88, 129, 161, 200, 251, 364), (15, 101, 160, 183, 227, 276), (15, 427, 515), (17, 89, 118), (17, 485, 564, 608, 693, 744, 793), (19, 79, 110, 211, 293, 332), (19, 478, 543, 675, 720, 777, 804, 828), (21, 67, 90, 185, 233), (22, 107, 135, 399, 422, 460, 491, 552, 592, 636, 783, 833), (23, 59, 100, 132, 147, 163, 190, 237, 308, 341, 407, 443, 530, 567, 601, 692, 715), (23, 132, 163, 237, 341, 443, 567, 692, 782, 805, 826), (23, 163, 308, 443, 601, 782, 826), (23, 190, 341, 530, 692, 805), (24, 450, 477, 492, 512, 560, 591), (25, 69, 99, 131, 168, 202, 257), (25, 131, 202, 305, 358, 398, 435, 479, 537, 599, 620, 657, 766, 810, 834), (25, 168, 305, 398, 479, 599, 657, 810), (26, 48, 91, 187, 389, 444, 466), (26, 91, 271, 297, 320, 350, 389), (26, 536, 578, 621, 652), (27, 53, 92, 133, 174, 213, 262, 299, 321, 354, 411, 456, 487, 553, 653, 678, 697, 734, 829), (29, 119, 144, 186, 246, 288), (29, 144, 246, 348, 380, 486, 513, 527, 633, 758, 822, 835), (30, 56, 145, 191, 247, 322, 360), (31, 75, 471, 679, 704, 736, 757, 821), (32, 113, 424, 451, 497, 542, 579, 622), (32, 162, 195, 239, 304), (33, 80, 148, 216), (33, 462, 528), (34, 61, 86, 102, 130, 159), (36, 103, 157, 198, 250, 298, 318, 378), (36, 425, 448, 516, 575), (37, 76, 111, 236), (37, 111, 303, 357, 386, 440, 496, 568, 609, 643, 682, 712), (38, 121, 214, 252, 327, 371, 433), (39, 96, 126, 171, 204, 221, 248, 316, 367, 381, 457, 483, 531, 572, 641, 690, 729), (40, 156, 232, 352, 415, 423, 452), (42, 409, 474, 510, 548, 605, 642, 677, 694), (44, 87, 125, 167), (44, 125, 369, 410, 459), (47, 72, 109, 203, 267, 335, 373), (48, 536, 621, 738, 774, 831), (49, 63, 122, 240, 346, 390), (52, 98, 136, 192, 220, 309), (64, 177, 253, 306, 356, 393), (64, 436, 545, 594, 638, 664, 716, 749, 839), (69, 537, 657, 834), (77, 105, 165, 193, 363, 441, 538), (79, 426, 478), (80, 379, 416, 462), (83, 222, 274, 313, 351, 442), (85, 197, 353, 388, 434, 450, 492, 560, 656, 681, 708, 746, 773), (85, 434, 477, 560, 681, 746, 817, 830), (89, 429, 485), (90, 282, 342, 430, 494), (95, 166, 208, 260, 345, 464, 508), (104, 170, 231, 310, 385, 401, 461, 514), (106, 134, 188, 234, 272, 292), (107, 178, 228, 302, 355, 399, 460, 552, 783), (107, 228, 355, 422, 491, 592, 783), (107, 302, 399, 491, 636), (108, 128, 176, 215, 263, 301, 319, 365, 402, 471), (112, 414, 523, 707, 801), (112, 458, 583, 801), (115, 141, 172, 325, 397), (119, 246, 380, 527, 835), (120, 173, 254, 294, 409, 510, 605, 677, 737, 784), (120, 254, 409, 548, 642, 694), (123, 197, 450), (127, 180, 209, 255, 340), (138, 179, 256), (138, 229, 256), (140, 201, 286, 326, 383), (142, 194, 285, 368, 472), (154, 206, 269, 343, 374, 413, 449, 480), (158, 241, 271, 320, 389), (162, 239, 349, 391, 451), (164, 377, 419), (165, 265, 363), (182, 329, 454), (184, 223, 324, 347, 370, 428), (186, 380), (217, 279, 314, 361, 417), (219, 268, 331, 384), (266, 336, 438), (474, 548, 677, 784), (475, 533, 582, 616, 658), (484, 518, 559, 618), (504, 555, 607, 631, 669, 709), (506, 532, 581, 626, 718, 799, 827), (517, 595, 663, 691, 823), (535, 590, 606, 630, 655, 676, 699, 741, 772, 808), (549, 588, 628, 670, 761), (569, 615, 701, 742), (580, 634, 662, 719, 735, 771, 811), (584, 649, 695, 726), (596, 639, 689), (602, 613, 688, 727, 751, 803, 840), (603, 732), (611, 627, 665, 710, 768), (617, 666, 794), (619, 645, 713, 764, 819), (623, 647, 702, 733, 770, 812), (624, 683, 723, 753, 807, 841), (637, 673, 728, 756, 787), (644, 661, 685, 724, 769, 809), (659, 740, 818), (668, 755), (680, 747, 820)))



plt.show()


