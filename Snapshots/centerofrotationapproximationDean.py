import csv
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import math
import readCases as rc

snapshots = []
snapind = -1
xsnapshots = []
ysnapshots = []
rowind = 0
masteri = 0
filelocation = 'Case1Clean.csv'

snapshots, xsnapshots, ysnapshots = rc.readComplexCases(filelocation)
structuralmarkers_0 = []
structuralmarkers_1 = []

#Snapshots you want to compare
snapcompare1 = 0
snapcompare2 = 125

#Gather the coordinates of the datapoints of 2 snapshots from all the snapshots
for i in range(len(xsnapshots[0])):
    structuralmarkers_0.append([xsnapshots[snapcompare1][i],ysnapshots[snapcompare1][i]])
    structuralmarkers_1.append([xsnapshots[snapcompare2][i],ysnapshots[snapcompare2][i]])

vectors0 =  structuralmarkers_0
vectors1 = structuralmarkers_1
print("Blue: ", vectors0,"\nOrange: ",vectors1)

anglerange = 0.088 # max angle [rad] / 5 deg
s = 30 #number of different angles for iteration
ds = anglerange / s #rad
angles = [round((i*ds),5) for i in range(s)] #array with every angle for iteration

def sysofeqs(x,y,xp,yp,theta): #system of equations 
    eq1 = x*math.cos(theta)-y*math.sin(theta) - xp
    eq2 = x*math.sin(theta)+y*math.cos(theta) - yp
    return eq1,eq2

xtransl = 625 #narrows down searching field in x direction/origin displacement
ytransl = 600 #narrows down searching field in y direction/origin displacement
dx = 1 #stepsize x
dy = 1 #stepsize y

result = [] 
count = 0 

#Computation of the vectors with respect to the new (displaced) origin
for vector in vectors0:
    vector[0] = round((vector[0]+ xtransl),3)
    vector[1] = round((vector[1]-ytransl),3)
for vector in vectors1:
    vector[0] = round((vector[0]+ xtransl),3)
    vector[1] = round((vector[1]-ytransl),3)

#Finds angle for which the rotation of all the points is equal and the
while len(result) == 0:
    match =7 #The number of data points that have to satisfy the system of equations
    for angle in angles:
        check = 0 #counter which checks how many pairs of datapoints (new and old) match with the rotation
        for i in range(len(vectors0)):
            dif1,dif2 = sysofeqs(vectors0[i][0],vectors0[i][1],vectors1[i][0],vectors1[i][1],angle)  #the difference of every requirement (equation)
            if (np.abs(dif1) <= 1) and (np.abs(dif2) <=1):
                check += 1
                if check == match: #checks whether enough pairs meet the demanded number of matches
                    result.append(angle)
                                        
    if count == 200: #limits the number of x iterations per dy iteration
        #Translations to the all the vectors of the data points with respect to the origin are made
        for vector in vectors0:
            vector[1] = round((vector[1]-dy),3) 
            vector[0] = vector[0] -xtransl
        for vector in vectors1:
            vector[1] = round((vector[1]-dy),3)
            vector[0] = vector[0] -xtransl
        count = 0 #serves as a counter for every dx per while loop
        xtransl = 625 #narrows down the field in x direction again
        ytransl += dy
    print("xtranslation of the origin: ",xtransl)
    print("ytranslation of the origin: ",ytransl)
    xtransl += dx
    #Translations to the all the vectors of the data points with respect to the origin are made
    for vector in vectors0:
        vector[0] = round((vector[0]+ dx),3)
    for vector in vectors1:
        vector[0] = round((vector[0]+ dx),3)
    count += 1
    print("Iteration: ",count)
    print("vectors0: ",vectors0)
    print("vectors1: ", vectors1)
print("angle: ",result[0],"[rad]")
print("The estimated center of rotation is at (",-xtransl,", ",ytransl,") based on a match of ", match," pairs of datapoints.")

plt.scatter(xsnapshots[snapcompare1],ysnapshots[snapcompare1])
plt.scatter(xsnapshots[snapcompare2],ysnapshots[snapcompare2])
plt.scatter(-xtransl,ytransl)
plt.show()
