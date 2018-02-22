# makeCoords.py
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



coords = []
with open('randomCoords.csv','w') as coordFile:
	for i in range(0,100): #get x number of random coordinates
		coords.append(getRandomCoordinate())
		coordFile.write(str(coords[i].ra.to_string(unit=u.hour))+','+str(coords[i].dec)+'\n')
coordFile.close()