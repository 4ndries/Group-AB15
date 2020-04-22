
#Packages
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import interp1d
from scipy import interpolate

#Iterative variables
i = 0
n = -1

#Raw data
Snapshots = []
Data = []
Value = []
xx = []
yy = []
zz = []
xsnaps = [] #Array of x points for several snapshot
ysnaps = [] #Array of y points for several snapshot
nsnaps = [0,100,200,300] #number of snapshots desired


#Read and process loop
for masteri in range(len(nsnaps)):

    #Reset variables at start of loop
    Snapshots = []
    Data = []
    Value = []
    xx = []
    yy = []
    zz = []

    #Read snapshot
    i = 0
    n = -1
    rawData = open(r"C:\Users\mateo\Documents\python\ProjectTest\Case0.dat" , "r")
    lines = rawData.readlines()
    rawData.close()

    #Data retrieval Outputs 1d arrays for each variable
    for line in lines:
        columns = line.split(" ")
        if "ZONE T" in line:
            n += 1 #Current snapshot
        if len(columns) == 13 and n == nsnaps[masteri]: #Tells program which snapshot to record
            columns = line.split(" ")
            x = float(columns[0].strip())
            y = float(columns[1].strip())
            z = float(columns[2].strip())
            I = columns[3].strip()
            u = columns[4].strip()
            v = columns[5].strip()
            w = columns[6].strip()
            lVl = columns[7].strip()
            trackID = int(columns[8].strip())
            ax = columns[9].strip()
            ay = columns[10].strip()
            az = columns[11].strip()
            lal = columns[12].strip()


            xx.append(x) #Raw x data
            yy.append(y) #Raw y data
            zz.append(z) #Raw z data


            Value.append([x,y,z])
            Data.append(Value)
            i = i + 1

    #Function: Datamakecolumn
    #Input: x [array] len(n), y[array] len(n)
    #Output: xcols [array] len(n), ycols [array] len(n)
    # Takes snapshot x, y data and groups them per markers column and outputs x and y coordinates of points in  each column

    def datamakecolumn(x,y):

        #Local function variables
        xcols = []
        ycols = []
        xcolsum =[]

        #Make Columns
        for i in range(len(x)):

            #First column entry
            xcurrentcol = [x[i]]
            ycurrentcol =[y[i]]

            #Group points from same column based on error squared (threshold)
            for j in range(len(x)):
                if abs(x[i]-x[j])**2 + abs(y[i]-y[j])**2 <= 150  and j != i:
                    xcurrentcol.append(x[j])
                    ycurrentcol.append(y[j])

            #Delete non-unique answers by checking if sum of array already appeared and length of column
            if round(np.sum(xcurrentcol)) not in xcolsum and len(xcurrentcol) >= 3:
                xcolsum.append(round(np.sum(xcurrentcol)))
                xcols.append(xcurrentcol)
                ycols.append(ycurrentcol)

        return xcols , ycols #Output x, y coordinates of points in each column (Array of Arrays)

    #Invoke function
    xcols , ycols = datamakecolumn(xx,yy)

    #Reset sd filter variables
    xfinalcols = []
    yfinalcols = []
    xcurrentfinalcols = []
    ycurrentfinalcols = []


    #Function: column standard deviation filter
    #Input: x [array] len(n), y[array] len(n), array containing markers coordinates per column
    #Output: xfinalcols [array] len(n), yfinalcols [array] len(n), array containing standard deviation filtered coordinates per column
    #Takes column coordinates and uses the sample standard deviation to filter out values more than three sigmas away

    def columnstdfilter(x,y):
        for i in range(len(x)):

            #Reset variables
            xcurrentfinalcols = []
            ycurrentfinalcols = []

            #Get column standard deviation and mean
            sd = np.std(x[i])
            xmean = np.average(x[i])
            ymean = np.average(y[i])

            #Check whether value within mean +- 3 standard deviation
            for j in range(len(x[i])):

                #Condition for 3 sigmas
                if  abs(x[i][j] - xmean)**2 + abs(y[i][j] - ymean)**2 <= 9*sd**2:
                    xcurrentfinalcols.append(x[i][j])
                    ycurrentfinalcols.append(y[i][j])
            xfinalcols.append(xcurrentfinalcols)
            yfinalcols.append(ycurrentfinalcols)

        return xfinalcols, yfinalcols #Column coordinates standard deviation filtered

    #Invoke function
    xfinalcols , yfinalcols = columnstdfilter(xcols,ycols)

    #Reset average variables
    xmean = []
    ymean = []

    #Function: column average
    #Input: x [array] len(n), y [array] len(n)
    #Output: xmean [array] len(n), ymean [array] len(n)
    #Takes sd filtered column coordinates and gets single coordinate for each column i.e. average position of points within a column

    def columnaverage(x,y):

        #Reset average variables
        xmean = []
        ymean = []

        #Average loop
        for i in range(len(x)):
            xaveragei = np.average(x[i])
            yaveragei = np.average(y[i])
            xmean.append(xaveragei)
            ymean.append(yaveragei)
        return xmean, ymean #Array with x,y coordinate of average position of each column

    #Invoke function
    xmean, ymean = columnaverage(xfinalcols, yfinalcols)


    #Function: Change of origin
    #Input: x [array] len(n), y [array] len(n), x0 [int/float], y0 [int/float]
    #Output: xtrue [array] len(n), ytrue [array] len(n)
    #Takes minimum of sample check distrance to x0, y0, apply correction to all points so that minimum is at x0, y0

    def changeorigin(x,y,x0,y0):

        xdiff = (x0-np.amin(x))
        ydiff = (y0-np.amin(y))

        xshift = []
        yshift = []

        for i in range(len(x)):

            xshifti = x[i]+xdiff
            yshifti = y[i]+ydiff
            xshift.append(xshifti)
            yshift.append(yshifti)

        return xshift, yshift #Shifted x, y coordinates

    #Invoke function
    xtrue, ytrue = changeorigin(xmean,ymean,0,0)

    #Append average column coordinate for each snapshot
    xsnaps.append(xmean)
    ysnaps.append(ymean)

#Plot variables
code = ['ro', 'bo', 'yo', 'go'] #Plot color
intercode = ['r-','b-', 'y-', 'g-' ] #Interpolant color
ss = [str(nsnaps[0]),str(nsnaps[1]),str(nsnaps[2]),str(nsnaps[3])] #Plot legend
interlegend = [str(nsnaps[0]) + ' interpolant',str(nsnaps[1]) + ' interpolant',str(nsnaps[2]) + ' interpolant',str(nsnaps[3]) + ' interpolant']

#Plot data
for i in range(len(xsnaps)):

    xnew = xsnaps[i]
    ynew = ysnaps[i]
    f = interp1d(xnew,ynew, 'cubic')
    xinter = np.linspace(np.amin(xsnaps[i]), np.amax(xsnaps[i]), 1000)
    yinter = f(xinter)

    plt.plot(xsnaps[i],ysnaps[i],code[i], label=ss[i])
    plt.plot(xinter,yinter,intercode[i], label=interlegend[i])

    plt.legend()

plt.show()







