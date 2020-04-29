import csv
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import readCases as rc

snapshots = []
snapind = -1
xsnapshots = []
ysnapshots = []
rowind = 0
masteri = 0
filelocation = 'Snapshots\Case1Clean.csv'

snapshots, xsnapshots, ysnapshots = rc.readComplexCases(filelocation)

for i in range(50):
    rand = random.randint(0,len(snapshots))
    plt.scatter(xsnapshots[i],ysnapshots[i])
plt.show()