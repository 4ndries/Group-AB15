import csv
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

#***Program that reads the csv files of case 1 nd case2**
#Input: case1Clean or case2Clean.csv (path) NOT CASE 0
#Output: snapshots, xsnapshots, ysnapshots, array are index matched ie snapshots[0] is the snapshot for the coordinates xsnapshot[0]
#Snapshots is a list of the snapshots saved
#Xsnapshots is the corresponding 8 x coordinates for that snap
#Ysnapshot smae but opposite

filelocation = 'Snapshots\Case1Clean.csv'


def readComplexCases(filelocation):

    snapshots = []
    xsnapshots = []
    ysnapshots = []

    with open(filelocation, 'r') as f:
        for line in f.read().split("\n")[0::3]:
            if line != '':
                linelist = line.split(',')
                snapshots.append(int(float(linelist[0])))

    with open(filelocation, 'r') as f:
        for line in f.read().split('\n')[2::3]:
            if line != '':
                linelist = line.split(',')
                numlist = [float(jk) for jk in linelist]
                xsnapshots.append(numlist)
    with open(filelocation, 'r') as f:
        for line in f.read().split('\n')[1::3]:
            if line != '':
                linelist = line.split(',')
                numlist = [float(jk) for jk in linelist]
                ysnapshots.append(numlist)
    return snapshots,xsnapshots,ysnapshots