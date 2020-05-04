import readCases as rc
import matplotlib.pyplot as plt
import numpy as np

snapshots,xsnapshots,ysnapshots = rc.readComplexCases('Snapshots\Case2TrackIDClean.csv')
snapi = np.arange(len(xsnapshots)//11,len(xsnapshots)//10)
for i in snapi:
    plt.scatter(xsnapshots[i],ysnapshots[i], label='Snapshots %s' % snapshots[i])

plt.show()

