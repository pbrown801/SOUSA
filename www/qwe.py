import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import asd
import itertools


filter1 = sys.argv[1]
filter2 = sys.argv[2]
filter3 = sys.argv[3]
filter4 = sys.argv[4]

os.chdir(os.path.expanduser('~/Dropbox/SN/madison/'))



####open type files and initilialize type lists######
with open('typeia.txt','r') as ias:
	typeia = [names.strip()for names in ias]


with open('typeibc.txt','r') as ibcs:
	typeibc = [names.strip()for names in ibcs]


with open('typeii.txt','r') as iis:
	typeii = [names.strip() for names in iis]


	
ia, ibc, ii = [],[],[]
type= []


snfiles = []
data = []
allofthem = []
count = 0
plt.ion()
plt.figure()


os.chdir(os.path.expanduser('~/Dropbox/SN/SOUSA/data'))


for i in os.listdir(os.path.expanduser('~/Dropbox/SN/SOUSA/data')):
	if i.endswith('15.1.dat'):
		snfiles.append(i[:-14])
for sn in snfiles:
    
    if sn in typeia:
        ia.append(sn)
    if sn in typeibc:
        ibc.append(sn)
    if sn in typeii:
	ii.append(sn)
	
    else:
	count +=1
ibc.remove('SN2012cw')  
'''
	if sn in typeic:
		ic.append(sn)
	if sn in typeiip:
		iip.append(sn)
	if sn in typeiin:
		iin.append(sn)
'''

	



#type.extend([ia,ibc,ii])



def foreachtype(typelist,colorstyle, markertype, axisnum):
    m = itertools.cycle(['o','^','*','s','D'])
    c = itertools.cycle(['b','r','m','c','g'])
    for each in typelist:
         print each
         eachline = asd.findingsn(each)
         print eachline
         mjdgrouped = asd.sortandgroup(eachline)
         colorseriesx, mag1x,mag2x,errorseriesx = asd.colorseries(mjdgrouped,filter1, filter2)
         colorseriesy,  mag1y,mag2y,errorseriesy = asd.colorseries(mjdgrouped,filter3,filter4)
		#timeseries = asd.epochseries(mjdgrouped, filter1, filter2)
         if len(colorseriesx) > len(colorseriesy):
             colorseriesy = np.append(colorseriesy,np.repeat(np.nan,len(colorseriesx)-len(colorseriesy)))
         if len(colorseriesy) > len(colorseriesx):
			colorseriesx = np.append(colorseriesx,np.repeat(np.nan,len(colorseriesy)-len(colorseriesx)))
         if len(errorseriesy) > len(errorseriesx):
			errorseriesx = np.append(errorseriesx,np.repeat(np.nan,len(errorseriesy)-len(errorseriesx)))
         if len(errorseriesx) > len(errorseriesy):
			errorseriesy = np.append(errorseriesy, np.repeat(np.nan,len(errorseriesx)-len(errorseriesy)))
         plt.plot(colorseriesx,colorseriesy, marker=markertype, markerfacecolor= colorstyle, linestyle='None')
         plt.errorbar(colorseriesx, colorseriesy,xerr=errorseriesx, yerr = errorseriesy, ecolor=colorstyle, fmt='none')
         #return colorseriesx, colorseriesy, errorseriesx, errorseriesy
 




os.chdir(os.path.expanduser('~/Dropbox/SN/madison/'))

