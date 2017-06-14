#query coordinates
from astropy import units as u
from astropy import coordinates

from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,ICRS,SkyCoord

import math

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

def tableFill(dam, ra, dec, appender,nme):
	t = Table(None) 
	Am = Column(name = 'Arcminute')
	North = Column(name = 'North')
	East = Column(name = 'East')
	South = Column(name = 'South')
	West = Column(name = 'West')
	t.add_columns([Am,North, East, South, West])
	A_v = []
	curVal = [None] *4 #n = 0, e = 1, s = 2, w = 3
	coord = [None] *4 #n = 0, e = 1, s = 2, w = 3
	#get values for each arcminute
	for j in range(0,dam+1):
		fourCoord(j, ra, dec, coord)
		t.add_row()
		t[j][0]=j
		for i in range(0,4):
			C = coordinates.SkyCoord(coord[i])
			table = IrsaDust.get_extinction_table(C.fk5)
			curVal[i] = (table['A_SandF'][2])
			t[j][i+1] = curVal[i]
			curVal = curVal[:]
	#	print(j,": ",coord)    #used to print the coordinates for checking
		A_v.append(curVal)
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
	return A_v;  #gets the data from IRSA database and stores A_v in array

def grabImage(ra,dec):
	imagelist = IrsaDust.get_image_list(SkyCoord(ra,dec).fk5, image_type="100um", radius=5*u.deg)
	image_file = download_file(imagelist[0],cache=True)
	image_data.append(fits.getdata(image_file, ext=0)) #gets image from IRSA database

def PicSaver(image_data,lists):

	if(len(start_coord)>5):
		go = 5
		iend = go
		sz1 = (int(len(lists))//go)+1
		sz2 = (int(len(lists))-(go*(sz1-1)))
	else:
		go = len(lists)
		iend = go
		sz1 = (int(len(lists))//go)
		sz2 = (int(len(lists))-(go*(sz1-1)))
	for j in range(0,sz1):
		if j==sz1-1:
			iend = sz2
		if iend == 1:
			plt.figure(1)
			plt.title(lists[len(lists)-1])
			plt.imshow(image_data[len(image_data)-1],cmap='gray')
			plt.colorbar()
			plt.savefig(lists[len(lists)-1]+".png")
		else:
			f, axarr = plt.subplots(1,iend)
			for i in range(go*(j),((j)*go)+iend): 
				im = axarr[i-(go*j)].imshow(image_data[i],cmap='gray')
				axarr[i-(go*(j))].set_title(lists[i])
			f.subplots_adjust(right=0.8)
			cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
			f.colorbar(im,cax = cbar_ax)
			f.savefig(lists[go*(j)]+".png")
			plt.clf()

	#-----Saves Graphs and Data To The Directory-----# #saves all images in .png files

from astropy.coordinates import name_resolve

#-----SETUP-----#

lists = []
start_coord = []

num = input("Enter galaxies separated by commas: Ex. M82, M83\n") #gets galaxies from user
for x in num.split(','):
	lists.append(x.strip()) #separates the commas and stores names in list
for i in range(0,len(lists)):
	tcoord=SkyCoord.from_name(lists[i],frame ='icrs') #gets coordinate from name given and stores in temporary SkyCoord
	start_coord.append(tcoord) #puts temporary SkyCoord in a list

dam = input('How many arcminutes?')
dam = int(dam)

from astropy.table import Table
from astropy.table import Column

#-----SETUP-----#

#------MAIN FUNCTION-----#

from astropy.utils.data import download_file
from astropy.io import fits
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
image_data = []

ra = Angle(start_coord[0].ra.hour,unit = u.hour) #gets radius of 1st coordinate as an angle (needed for things to work)
dec = start_coord[0].dec #dont need an angle for some reason but it works


x = np.arange(dam+1) #creates array of size dam+1 to store values

appender = 'w' #lets us overwrite a file or make a new one
nme = lists[0]
A_v = tableFill(dam,ra,dec,appender,nme) #runs the main functionality and returns the data of a galaxy
grabImage(ra,dec) #gets image data and stores in list
appender = 'a' #lets us append a file instead of overwriting
for i in range(1,len(start_coord)):
	nme = lists[i]
	ra = Angle(start_coord[i].ra.hour,unit = u.hour)
	dec = start_coord[i].dec
	A_v = tableFill(dam,ra,dec,appender,nme)
	grabImage(ra,dec)
PicSaver(image_data,lists) #saves all images in .png files, don't mess with this


A_v = np.array(A_v) #stores values in numpy array
# plt.figure(2)
# plt.plot(x,A_v[:,0], color = "blue", marker = ".", label = "North")
# plt.plot(x, A_v[:,1], color = "red", marker = ".", label = "East")
# plt.plot(x, A_v[:,2], color = "green", marker = ".", label = "South")
# plt.plot(x, A_v[:,3], color = "black", marker = ".", label = "West")
# plt.title("A_v Values by Arcminute")
# plt.xlabel("Arcminutes from Center of Star")
# plt.ylabel("A_v Value")
# plt.legend(loc='lower left', shadow=True)
# plt.show(block = True)
