# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:35:32 2016

@author: aggienova
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import asd
import matplotlib.lines as mlines
import qwe
filter1 = qwe.filter1
filter2 = qwe.filter2
filter3 = qwe.filter3
filter4 = qwe.filter4

 
qwe.foreachtype(qwe.ia,'r', 'o', 1)
qwe.foreachtype(qwe.ibc,'b','*',1)
'''
foreachtype(ic,'g','s',1)
foreachtype(iip, 'm','v',1)
foreachtype(iin,'c','D',1)
'''
qwe.foreachtype(qwe.ii,'k','^',1)


ias = mlines.Line2D([],[],marker='o',color='r',label='Ia')
ibcs = mlines.Line2D([],[],marker='*',color='b',label='Ibc')
'''
ics = mlines.Line2D([],[],marker='s',color='g',label='Ic')
iips = mlines.Line2D([],[],marker='v',color='m',label='IIP')
iins = mlines.Line2D([],[],marker='D',color='c',label='IIn')
'''
iis = mlines.Line2D([],[],marker='^',color='k',label='II')


######Trying to figure out the subplot thing here#######
''''
filters = ['UVW2','UVW1','UVM2','U','B','V']
combos = list(itertools.combinations(filters,2))
for axis in range(len(combos)):
	foreachtype(ia,'r', 'o',axis)
	foreachtype(ib,'b','*',axis)
	foreachtype(ic,'g','s',axis)
	foreachtype(iip, 'm','v',axis)
	foreachtype(ii,'k','^',axis)
	foreachtype(iin,'c','D',axis)
'''

plt.legend(handles=[ias,ibcs,iis], title="SN Types")



ylabel = filter1 + '-'+filter2
xlabel = filter3 + '-' + filter4
plt.xlabel(xlabel)
plt.ylabel(ylabel)
#plt.legend()
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)

plt.show()		

