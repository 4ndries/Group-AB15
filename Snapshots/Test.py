import readCases as rc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

snapshots,xsnapshots,ysnapshots = rc.readComplexCases('Snapshots\Case2BTrackIDClean.csv')
snapi = np.arange(0,len(xsnapshots))


fig = plt.figure()
ax = plt.axes(xlim=(xsnapshots[0][0]-50, xsnapshots[0][-1]+50), ylim=(ysnapshots[0][0]-50, ysnapshots[0][-1]+50))
line, = ax.plot([], [],'ro', lw=3)
def init():
    line.set_data([],[])
    return line,

def animate(i):
    x = xsnapshots[i]
    y = ysnapshots[i]
    line.set_data(x,y)
    return line,

plt.title('Case2 Movement')
plt.axis('off')
anim = animation.FuncAnimation(fig,animate,init_func=init,frames=5000,interval=10,blit=True)
plt.show()
#anim.save('Snapshots\Animation.gif', writer='imagemagick', fps=30)


