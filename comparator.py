#this is going to graph shit

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import itertools
import os.path


csv = np.genfromtxt ('K_tot Values.csv',delimiter=",")
kvals = csv[:,1]
print(kvals)
csv = np.genfromtxt('A_v Values.csv',delimiter=",")
avals = csv[:,1]
print(avals)

names = ['NGC6946','NGC3344','NGC55','NGC300','M101','NGC4214','NGC4424','NGC4258','NGC5194','NGC5128','m83', 'm82']

plt.clf()
plt.figure(1)
plt.scatter(kvals,avals)
plt.xlabel("A_v Value")
plt.title("K_tot by A_v")
plt.ylabel("K_Tot Value")
scatter_names = []
for i in range(len(kvals)):
	scatter_names.append(plt.scatter(kvals[i],avals[i]))
from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')
plt.legend((scatter_names),(names),scatterpoints=1,ncol=4,fontsize=8,prop=fontP,bbox_to_anchor=(0,1.03,1,.2),mode="expand",loc='lower left')


labels = ['{}'.format(i) for i in range(len(kvals))]


for label, x, y in zip(labels, kvals[:], avals[:]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(20, 0),
        textcoords='offset points', ha='right', va='bottom',
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig(os.path.join('Graphs'," K_Tot Scatter.png"))
fig.savefig('test2.png', dpi=100)
plt.show()