 #	 Copyright 2017 Tate M. Walker

 #   Licensed under the Apache License, Version 2.0 (the "License");
 #   you may not use this file except in compliance with the License.
 #   You may obtain a copy of the License at

 #       http://www.apache.org/licenses/LICENSE-2.0

 #   Unless required by applicable law or agreed to in writing, software
 #   distributed under the License is distributed on an "AS IS" BASIS,
 #   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 #   See the License for the specific language governing permissions and
 #   limitations under the License.


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print(chr(27) + "[2J")
    sys.stdout.write('\rDone!')

def AvFill(ra,dec): # get AV Schafly Values
	coord = ra.to_string()+" "+dec.to_string()
	coord = coordinates.SkyCoord(coord, frame = 'fk5')
	table = IrsaDust.get_extinction_table(coord, show_progress = False)
	# table.show_in_browser('chrome')
	return table['A_SandF'][2]

def getLink(name):
	link = "https://ned.ipac.caltech.edu/cgi-bin/objsearch?"
	inputs = {'objname': name,
				'extend': 'no',
				'hconst': '73',
				'omegam': '0.27',
				'omegav': '0.73',
				'corr_z': '1',
				'out_csys': 'Equatorial',
				'out_equinox': 'J2000.0',
				'obj_sort': "RA or Longitude",
				'of': 'pre_text',
				'zv_breaker': '30000.0',
				'list_limit': '5',
				'img_stamp': 'YES'}
	page = requests.get(link, params = inputs)
	from bs4 import BeautifulSoup
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup

def Morphology(name):
	try:
		soup = getLink(name)
		soup = soup.find("a", attrs={'name':'BasicData_0'})
		morphology = soup.next_sibling.next_sibling.next_sibling.find("pre")
		morphology = list(morphology.children)[2]
		morphology = (morphology.split(": ",4)[4]).rstrip()
		return morphology
	except (IndexError, AttributeError) as e:
		morphology = None
		return morphology

def Redshift(name):
	try:
		soup = getLink(name)
		soup = soup.find("a", attrs={'name':'BasicData_0'})
		soup = soup.next_sibling.next_sibling.next_sibling.find("pre")
		redshift = list(soup.children)[1]
		redshift = str(redshift).split(">",1)[1]
		redshift = redshift.split("<",1)[0]
		return(redshift)
	except (IndexError, AttributeError) as e:
		redshift = None
		return redshift

def LatLong(name):
	try:
		soup = getLink(name)
		soup = soup.find("a", attrs={'name':'Positions_0'})
		coords = soup.next_sibling.next_sibling.find("pre")
		coords = list(coords.children)[4]
		coords = (coords.split("Galactic ",1)[1]).lstrip()
		longitude = (coords.split()[0])
		latitude = (coords.split()[1])
		coords = [str(longitude),str(latitude)]
		return coords
	except (IndexError, AttributeError) as e:
		coords = [None,None]
		return coords

def scrapeValues(name):
	soup = getLink(name)
	#----------Get Velocities----------#
	try:
		soup = soup.find("a", attrs={'name':'DerivedValues_0'})
		velocities = soup.next_sibling.next_sibling.next_sibling.find("pre")
		Helio = list(velocities.children)[2]
		VGS = list(velocities.children)[16]
		Helio = Helio.lstrip('\n')
		VGS = VGS.lstrip('\n')
		Hvals = [int(s) for s in Helio.split() if s.isdigit()]
		VGSVals = [int(s) for s in VGS.split() if s.isdigit()]
		vels = [Hvals[0],Hvals[1],VGSVals[0],VGSVals[1]]
		return vels
	except (IndexError, AttributeError) as e:
		vels = [None,None,None,None]
		return vels

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
from utlilities import *

done = False
print(chr(27) + "[2J")
threader = threading.Thread(target=animate)
threader.start()

gals = read_gals('input.txt') #read in galaxies from input file
[gals, start_coord] = get_coords(gals) #grab coordinates given galaxy list

write_file = 'scriptData.csv'

with open(write_file,'w') as output:
	output.write("Name, Ra, Dec, Lat, Long, Av, Morph, Red, Helio, Error, VGS, Error, \n")
for i in range(0,len(gals)):
	[ra,dec] = coord_breakup(start_coord[i])
	Av = AvFill(ra, dec)
	redshift = Redshift(gals[i])
	vels = scrapeValues(gals[i])
	morphology = Morphology(gals[i])
	coords = LatLong(gals[i])
	with open(write_file, 'a') as output:
		output.write(gals[i] + ',' + ra.to_string() + ',' + dec.to_string() + ',' + coords[0] + ',' + coords[1] + ',' + str(Av) + ',' + str(morphology) + ',' + str(redshift) + ',' + str(vels[0]) + ',' + str(vels[1]) + ',' + str(vels[2]) + ',' + str(vels[3]) + '\n')
		print(gals[i] + " Done!")
done = True
