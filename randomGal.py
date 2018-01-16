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

def timeFix(s,m,h): #fixes time to ensure it stays within normal range (0-60)
	if(s>=60 or m>=60):
		while(s>=60 or m>=60):
			if s >= 60:
				m+=1
				s-=60
			if m >= 60:
				h+=1
				m-=60
	elif(s<0 or m<0):
		while(s<0 or m<0):
			if s < 0:
				m-=1
				s+=60
			if m < 0:
				h-=1
				m+=60		
	return s,m,h;


def fourCoord(dam,ra,dec,coord):

	ds = dam*4

	#e
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h)
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	coord[1] = rad.to_string()+" "+dec.to_string()

	#n
	decli = dec.arcminute+dam
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	coord[0] = ra.to_string()+" "+decl.to_string()
	
	#w
	ds=ds*(-1)
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h)
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	coord[3] = rad.to_string()+" "+dec.to_string()

	#s
	decli = dec.arcminute-dam
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	coord[2] = ra.to_string()+" "+decl.to_string()
	
	#print(coord)
	return coord; #performs transformation of initial coord into cardinal coordinates 

def tableFill(dam, ra, dec):
	# curVal = [None] *4 #n = 0, e = 1, s = 2, w = 3
	coord = [None] *4 #n = 0, e = 1, s = 2, w = 3
	#get values for each arcminute
	for j in range(0,dam+1):
		fourCoord(j, ra, dec, coord)
		with open('randomAv.csv','a') as output:
			output.write(str(j)+',')
			for i in range(0,4):

				C = coordinates.SkyCoord(coord[i])
				table = IrsaDust.get_extinction_table(C.fk5, show_progress = False)
				output.write(str(table['A_SandF'][2])+',')
				# curVal[i] = (table['A_SandF'][2])	
			output.write('\n')

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print(chr(27) + "[2J")
    sys.stdout.write('\rDone!')


coords = []

for i in range(0,10): #get x number of random coordinates
	coords.append(getRandomCoordinate())
	# print(coords[i])

write_file = 'randomAV.csv'
arcMinutes = 5


# threading
done = False
print(chr(27) + "[2J")
threader = threading.Thread(target=animate)
threader.start()

with open(write_file,'w'):

	for i in range(0,len(coords)):

		with open(write_file,'a') as output:
			output.write(str(coords[i].ra.to_string(unit = u.hour)) + ',' + str(coords[i].dec.to_string()) + ", \n Arcminute, North, East, South, West,\n")
		tableFill(arcMinutes,coords[i].ra,coords[i].dec)
		print('\n'+str(len(coords)-i) + " left!")

done = True