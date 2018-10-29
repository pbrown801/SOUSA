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
	"""
		Converts csv file to ascii file
	"""
	outFile = outFile+'.txt'
	with open(outFile,'w') as output:
		with open(inFile) as csvinp:
			reader = csv.reader(csvinp,delimiter = ',')
			for row in reader:
				for col in row:
					output.write(str(col) + ' ')
				output.write('\n')

def read_gals(input_file,desired_col=0): #remember why i need this
	"""
		Reads in galaxies from different file types and parses them into a list of galaxies by name
		Returns:
			gals: list of galaxies from input file
	"""
	if input_file.endswith('.xlsx'):
		df = pd.read_excel(excel_input,header = 1, parse_col = desired_col)
		print(df)
		print(df['ra'])
	elif input_file.endswith('.csv'): #this part works
		gals = []
		with open(input_file) as inp:
			for row in inp:
				gals.append(row.split()[0])
	elif input_file.endswith('txt'):
		gals = []
		with open(input_file) as inp:
			gals = inp.read().splitlines()
	return gals

def get_coords(gals):
	"""
		Takes list of galaxies and looks up their coordinates by name.
		If no name found: warn, skip, remove galaxy from list

		Returns:
			gals: list of galaxies minus those that weren't found
			start_coord: list of coordinates corresponding to center of galaxies in 'gals'
	"""
	start_coord = []
	for i in gals[:]: #gets all valid galaxies
		try:
			print(i)
			tempCoord = SkyCoord.from_name(i, frame = 'icrs')
			start_coord.append(tempCoord)
		except NameResolveError:
			print('Skipping',i,'because it couldn\'t be found.')
			gals.remove(i)
	return(gals,start_coord)

def coord_breakup(coord):
	"""
		Breaks up a coordinate into its components
	"""
	ra = Angle(coord[i].ra.hour,unit = u.hour)
	dec = coord[i].dec
	return(ra,dec)


def timeFix(s,m,h):
	"""
		Fixes time to ensure it stays within normal range (0-60)
	"""
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
	return s,m,h

#------------------------AV Utility Functions Below------------------------#

def fourCoord(distance,ra,dec,cardinals):
	"""
		Gets four coordinates a specified distance away from the center of the galaxy
		Inputs:
			distance: distance in arcminutes
			ra: radial component of the coordinate
			dec: declination component of the coordinate
			cardinals: [None]*4 list with a spot for coordinate at each cardinal direction
		Outputs:
			cardinals: list of four coordinates *distance* arcminutes away from the center of the specified galaxy. (North, East, South, West)
	"""
	ds = distance*4

	#e
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h) #keep time within allowed range
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	cardinals[1] = rad.to_string()+" "+dec.to_string()

	#n
	decli = dec.arcminute+distance
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	cardinals[0] = ra.to_string()+" "+decl.to_string()

	#w
	ds=ds*(-1)
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h) #keep time within allowed range
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	cardinals[3] = rad.to_string()+" "+dec.to_string()

	#s
	decli = dec.arcminute-distance
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	cardinals[2] = ra.to_string()+" "+decl.to_string()

	#print(cardinals)
	return cardinals; #performs transformation of initial coordinate into cardinal coordinates

def tableFill(distance, ra, dec, appender,nme):
	"""
		IN THE PROCESS OF CLEANING THIS UP
		Things I think I don't need:
			Table
	"""
	t = Table(None)
	Am = Column(name = 'Arcminute')
	North = Column(name = 'North')
	East = Column(name = 'East')
	South = Column(name = 'South')
	West = Column(name = 'West')
	t.add_columns([Am,North, East, South, West])
	tA_v = []
	curVal = [None] *4 #n = 0, e = 1, s = 2, w = 3
	cardinals = [None] *4 #n = 0, e = 1, s = 2, w = 3
	#get values for each arcminute
	for j in range(0,distance+1):
		fourCoord(j, ra, dec, coord)
		t.add_row()
		t[j][0]=j
		for i in range(0,4):
			C = coordinates.SkyCoord(coord[i])
			table = IrsaDust.get_extinction_table(C.fk5, show_progress = False)
			curVal[i] = (table['A_SandF'][2])
			t[j][i+1] = curVal[i]
			curVal = curVal[:]
		tA_v.append(curVal)

	t.add_row()
	for i in range(0,5): #this adds a blank line to the table to separate queries
		t[j+1][i] = None
	n = [nme]
	namesTable = Table([n], names=('n'))
	final_name = namesTable.to_pandas()
	final_vals = t.to_pandas()
	from pandas import ExcelWriter
	with open('A_v Values.csv', appender) as f:
		final_name.to_csv(f, header =False, index = False)
	appender = 'a'
	with open('A_v Values.csv', appender) as f:
		final_vals.to_csv(f, header =True, index = False, sep = ',')
	return(tA_v)#gets the data from IRSA database and stores A_v in array
