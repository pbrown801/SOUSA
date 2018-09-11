# utilities.py

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
import csv
import pandas as pd
import requests
import threading
import time

def csv_to_ascii(inFile,outFile):
	outFile = outFile+'.txt'
	with open(outFile,'w') as output:
		with open(inFile) as csvinp:
			reader = csv.reader(csvinp,delimiter = ',')
			for row in reader:
				for col in row:
					output.write(str(col) + ' ')
				output.write('\n')

def read_gals(input_file,desired_col): #remember why i need this
	if input_file.endswith('.xlsx'):
		df = pd.read_excel(excel_input,header = 1, parse_col = desired_col)
		print(df)
		print(df['ra'])
	elif input_file.endswith('txt'):
		gals = []
		with open(input_file) as inp:
			gals = inp.read().splitlines()
	return gals

def get_coords(gals):
	start_coord = []
	for i in gals[:]: #gets all valid galaxies
		try:
			tempCoord = SkyCoord.from_name(i, frame = 'icrs')
			start_coord.append(tempCoord)
		except NameResolveError:
			gals.remove(i)
	return(gals,start_coord)

def coord_breakup(coord):
	ra = Angle(coord[i].ra.hour,unit = u.hour)
	dec = coord[i].dec
	return(ra,dec)