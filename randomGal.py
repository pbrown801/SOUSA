#randomGal.py

from astropy import units as u
from astropy import coordinates
from astroquery.ned import Ned
from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,ICRS,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
import math
import os.path
import sys

import itertools
import threading
import time

import requests
from astropy.coordinates import SkyCoord
from random import randint


#LOOK AT QUICKDATA.PY FOR MULTIPLE GALAXY CONFIG
def getRandomCoordinate():
	h = randint(0,23)
	# print("h = " + str(h))
	m = randint(0,59)
	# print("m = " + str(m))
	s = randint(0,59)
	# print("s = " + str(s))

	d = randint(-89,89)
	# print("d = " + str(d))
	arcm = randint(0,59)
	# print("arcm = " + str(arcm))
	arcs = randint(0,59)
	# print("arcs = " + str(arcs))
	
	ra = Angle((h, m, s), unit=u.hour) #creating right ascension angle
	dec = Angle((d, arcm, arcs), unit=u.deg) #creating declination angle
	# print(ra.to_string())
	# print(dec.to_string())
	return SkyCoord(ra, dec, frame = 'fk5')

# import pandas as pd:
import csv
def readCoordinate():
 	names = [None]*462 #there are 462 entries
 	read_file = 'cepheidGals.csv'
 	i = 0
 	with open(read_file) as csvinp:
 		reader = csv.reader(csvinp,delimiter = ',')
 		for row in reader:
 			names[i] = row[0]
 			try:
 				tcoord = SkyCoord.from_name(row[0],frame = 'icrs')
 				coords[i] = tcoord
 			except:
 				print(row[0])
 				i-=1
 			# ra = row[1]
 			# dec = row[2]
 			#SkyCoord(ra,dec,frame = 'fk5')
 			i+=1
 	return [names,coords]


def timeFix(s,m,h): #fixes time to ensure it stays within normal range (0-60)
	if(s>=60 or m>=60):
		while(s>=60 or m>=60):
			if s >= 60:
				m+=1
				s-=60
			if m >= 60:
				if h == 23:
					h = 0
					m-=60
				else:
					h+=1
					m-=60
	elif(s<0 or m<0):
		while(s<0 or m<0):
			if s < 0:
				m-=1
				s+=60
			if m < 0:
				if h == 0:
					h = 23
					m+=60
				else:
					h-=1
					m+=60		
	return s,m,h;



def fourCoord(dam,ra,dec,coord):

	ds = dam*4

	coord[0] = ra.to_string()+" "+dec.to_string()

	#n
	decli = dec.arcminute+dam
	if decli > 90:
		decli -=90
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	coord[1] = ra.to_string()+" "+decl.to_string()

	#e
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h)
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	coord[2] = rad.to_string()+" "+dec.to_string()

	#w
	ds=ds*(-1)
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h)
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	coord[4] = rad.to_string()+" "+dec.to_string()

	#s
	decli = dec.arcminute-dam
	if decli < 0:
		decli +=90
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	coord[3] = ra.to_string()+" "+decl.to_string()
	
	#print(coord)
	return coord; #performs transformation of initial coord into cardinal coordinates 

def tableFill(dam, ra, dec):
	curVal = [None] *5 #n = 0, e = 1, s = 2, w = 3
	coord = [None] *5 #n = 0, e = 1, s = 2, w = 3
	#get values for each arcminute
	for j in range(dam,dam+1): #change 1st dam to 0 for concurrent values
		coord = fourCoord(j, ra, dec, coord)
		for i in range(0,5):
			try:
				C = coordinates.SkyCoord(coord[i])
				table = IrsaDust.get_extinction_table(C.fk5, show_progress = False)
				curVal[i] = (table['A_SandF'][2])	
			except Exception as e:
				curVal = [None] * 5
				break
		# output1.write('\n')
	return curVal

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print(chr(27) + "[2J")
    sys.stdout.write('\rDone!')

# MAIN FUNCTION

if __name__ == '__main__':


	write_file = 'randomAV.csv'
	arcMinutes = 20

	done = False
	print(chr(27) + "[2J")
	threader = threading.Thread(target=animate)
	threader.start()
	coords = [None] * 462
	avData = [None] * len(coords)

	with open(write_file,'w') as output:
		output.write(str(arcMinutes) + " Arcminutes\nCenter, North, East, South, West\n")
		output.close()
	[names, coords] = readCoordinate()
	for i in range(0,len(coords)):
	# 	coords[i] = getRandomCoordinate()
		with open(write_file,'a') as output1:
			try:
				avData[i] = tableFill(arcMinutes,coords[i].ra,coords[i].dec)
				output1.write(str(names[i]) + ',' + str(coords[i].ra.to_string(unit = u.hour)) + ',' + str(coords[i].dec.to_string()) + '\n')
				for j in avData[i]:
					output1.write(str(j) + ',')
				output1.write('\n')
				output1.close()
				print('\n'+str(len(coords)-1-i) + " left!")
			except Exception as e:
				print(e)
					
				

	done = True

