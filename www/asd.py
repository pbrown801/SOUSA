
import numpy as np
from operator import itemgetter, attrgetter
import os
import collections


filter1 = 'UVW1'
filter2 = 'UVW2'

os.chdir(os.path.expanduser('~/Dropbox/SN/SOUSA/data'))

dt = 0.1500
global mjdgrouped
global dat
mjdgrouped = []
snname = 'SN005hk'

def findingsn(snname):
    

    #if os.path.isfile(snname+'_uvotB15.1.dat'):
    os.chdir(os.path.expanduser('~/Dropbox/SN/SOUSA/data'))
    dat = open(snname+'_uvotB15.1.dat','r')
    #os.chdir(os.path.expanduser('~/Dropbox/SN/madison'))
    #dat = open(snname + '_absolute.txt')


    with open(snname+'_uvotB15.1.dat','r') as dat:
    #with open(snname + '_absolute.txt','r') as dat:
            reading = np.genfromtxt(dat, dtype=[('filter', 'S20'),('mjd',float),('mag',float),('magerr',float)], usecols=(0,1,2,3), unpack= True)
    return reading
    





########Sorting SN into groups based on MJD +/- dt
def sortandgroup(lines):
     mjdsorted = sorted(lines, key=itemgetter(1))

	#ends = mjdsorted[0][1]
     mjdgrouped_uncorr = []
     mjdgrouped = []
     dates = []
     start = 0 
     count = 1



     mjds = []
     for j in mjdsorted:
         mjds.append(j[1])


     for i in range(len(mjdsorted)):
		if i ==0:
			start=0
		
		else:
			if mjdsorted[i][1] < mjdsorted[i-1][1] + dt:
				count +=1
		
			else:
				mjdgrouped_uncorr.append(mjdsorted[start:i])
				start = i
     mjdgrouped_uncorr.append(mjdsorted[start:])
     for j in mjdgrouped_uncorr:
         for m in range(len(j)):
             dates.append(len(j))
         if len(dates) != len(set(dates)):
             indiv = []
             repeat_check = 0
             repeated = [item for item, count2 in collections.Counter(dates).items() if count2 > 1]
             for byfilter in j:
                 if byfilter[0] in repeated:
                     repeat_check +=1
                     if repeat_check == 1:
                         indiv.append(byfilter)
                 if byfilter[0] not in repeated:
                     indiv.append(byfilter)
             mjdgrouped.append(indiv)
         if len(dates) == len(set(dates)):
             mjdgrouped.append(j)
                        
                        
     return mjdgrouped

#mjdgrouped = sortandgroup(lines)

def colorseries(mjdgrouped,filter1, filter2):
    mag1s = []
    mag2s = []
    error1temp = []
    error2temp = []
    errors = []
    dates = []
    for j in mjdgrouped:
        for m in range(len(j)):
             dates.append(j[m][0])   
                    
        if filter1 in dates and filter2 in dates:
            doublescheck1 = 0 
            doublescheck2 = 0
            fixingcount1 = 0
            fixingcount2 = 0

            for k in range(len(j)):
                if j[k][0] == filter1:
                    mag1s.append(j[k][2])
                    error1temp.append(j[k][3])
                    doublescheck1 += 1
                '''
                if doublescheck1 > 1:
                    while fixingcount1 <= doublescheck1:
					mag2s.append(np.nan)
					error2temp.append(np.nan)
					fixingcount1 += 1
              '''
                if j[k][0] == filter2:
                            mag2s.append(j[k][2])
                            error2temp.append(j[k][3])
                            doublescheck2 += 1
                '''
                if doublescheck2 > 1:
                    while fixingcount2 <= doublescheck2:
                            mag1s.append(np.nan)
                            error1temp.append(np.nan)
                            fixingcount2 += 1
			'''		
 
        if filter1 not in dates:
            
            mag1s.append(np.nan)
            error1temp.append(np.nan)
            for k in range(len(j)):
				if j[k][0] == filter2:
					mag2s.append(j[k][2])		
					error2temp.append(j[k][3])
     
        if filter2 not in dates:
            
		mag2s.append(np.nan)
		error2temp.append(np.nan)
		for k in range(len(j)):
			if j[k][0] == filter1:
					mag1s.append(j[k][2])
					error1temp.append(j[k][3])
        del dates[:]
    maga = np.asarray(mag1s)
    magb = np.asarray(mag2s)
    error1temps = np.asarray(error1temp)
    error2temps = np.asarray(error2temp)
    if len(error1temps) > len(error2temps):
        error1temps = error1temps[:-(len(error1temps)-len(error2temps))]
    
    		#error2temps = np.append(error2temps,np.repeat(np.nan,len(error1temps)-len(error2temps)))
    if len(error1temps) < len(error2temps):
        error2temps = error2temps[:-(len(error2temps)-len(error1temps))]
    		#error1temps = np.append(error1temps,np.repeat(np.nan,len(error2temps)-len(error1temps)))
    if len(maga) > len(magb):
        maga = maga[:-(len(maga)-len(magb))]
    		#magb = np.append(magb,np.repeat(np.nan,len(maga)-len(magb)))
    if len(magb) > len(maga):
        magb = magb[:-(len(magb)-len(maga))]
           #maga = np.append(maga,np.repeat(np.nan,len(magb)-len(maga)))

    errors = np.sqrt(error1temps**2 + (error2temps)**2)	
    color = maga-magb		
    return color, mag1s, mag2s, errors
#colorseries, mag1, mag2, errorseries= colorseries(mjdgrouped,filter1,filter2)

def epochseries(unavg, checkfilter1, checkfilter2):
    count = 0
    skip = 0
    num = 0	
    avgepoch = []

    '''
    for k in unavg:
        sum = 0
        num = 0
        for j in range(len(k)):
            if k[j][0] not in temp:
                temp.append(k[j][0])
                
        for step in range(len(k)):
            if checkfilter1 not in temp:
                avgepoch.append(np.nan)
            if checkfilter2 not in temp:
                avgepoch.append not in temp
            else:
                sum += k[step][1]
                num += 1.0
            
 
	'''
    for k in unavg:
         count = 0 
         num = 0
         temp = []
         for j in range(len(k)):
             if k[j][0] not in temp:	
			temp.append(k[j][0])
              
        
         if checkfilter1 not in temp:
            if checkfilter2 not in temp:
                skip += 1
                avgepoch.append(np.nan)
            if checkfilter2 in temp:
                avgepoch.append(np.nan)
                
                    
      
         else:
             for step in k:
                   count += step[1]
                   num += 1.0

				
    
		
         del temp [:]
         if num != 0:
            avgt = count/num
			#print "HEY THIS IS THE AVG OF THE EPOCH: " + str(avgt)
            avgepoch.append(avgt)	
            
    return avgepoch

def relative_time(colors, times):
    reltimeseries = []
    zipped = zip(colors, times)
    peak = max(zipped, key=lambda item:item[0])[1]
    for time in times:
        reltimeseries.append(time-peak)
    return reltimeseries, peak, zipped
	

os.chdir(os.path.expanduser('~/Dropbox/SN/madison/'))



#data.close()
