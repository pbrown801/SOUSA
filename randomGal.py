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

# galaxy = input("Enter galaxy followed by [Enter]\n")
# try:
# 	tempCoord = SkyCoord.from_name(galaxy, frame = 'icrs')
# except NameResolveError:
# 	print("Can't retrieve coordinates for galaxy, please check the name and try again.")

# >>> c = SkyCoord('00 42 30 +41 12 00', unit=(u.hourangle, u.deg))
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


coords = []
av = []

write_file = 'randomAV.csv'
with open(write_file,'w') as output:
	output.write("RA, DEC, AV \n")

for i in range(0,10): #get x number of random coordinates
	coords.append(getRandomCoordinate())
	print(coords[i])
	# print(coords[i].ra.to_string(unit = u.hour))
	table = IrsaDust.get_extinction_table(coords[i], show_progress = False)
	av.append(table['A_SandF'][2])
	print(av[i])

	with open(write_file, 'a') as output:
		output.write(str(coords[i].ra.to_string(unit = u.hour)) + ',' + str(coords[i].dec.to_string()) + ',' + str(av[i]) + '\n')


	





# done = False
# print(chr(27) + "[2J")
# threader = threading.Thread(target=animate)
# threader.start()

# write_file = 'randVals.csv'
# with open(write_file,'w') as output:
# 	output.write("\n")
# 	ra = Angle(tempCoord.ra.hour,unit = u.hour)
# 	dec = tempCoord.dec
	
# 	with open(write_file, 'a') as output:
# 		output.write( '\n')
# 		#print(gals[i] + " Done!")
# done = True