#query coordinates
from astropy import units as u
from astropy import coordinates

from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,ICRS,SkyCoord

import math
import os.path
import sys

import requests

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
	tA_v = []
	curVal = [None] *4 #n = 0, e = 1, s = 2, w = 3
	coord = [None] *4 #n = 0, e = 1, s = 2, w = 3
	#get values for each arcminute
	for j in range(0,dam+1):
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

def grabImage(ra,dec):
	imagelist = IrsaDust.get_image_list(SkyCoord(ra,dec).fk5, image_type="100um", radius=2*u.degree)
	image_file = download_file(imagelist[0],cache=True)
	image_data.append(fits.getdata(image_file, ext=0)) #gets image from IRSA database

def PicSaver(image_data,gals):

	if(len(start_coord)>5):
		go = 5
		iend = go
		sz1 = (int(len(gals))//go)+1
		sz2 = (int(len(gals))-(go*(sz1-1)))
	else:
		go = len(gals)
		iend = go
		sz1 = (int(len(gals))//go)
		sz2 = (int(len(gals))-(go*(sz1-1)))
	for j in range(0,sz1):
		if j==sz1-1: #if last set of five
			iend = sz2
		if iend == 1: #if only one plot remains
			plt.figure(1)
			plt.title(gals[len(gals)-1])
			plt.imshow(image_data[len(image_data)-1],cmap='gray')
			plt.colorbar()
			plt.savefig(os.path.join('Pictures',(gals[len(gals)-1]+".png")))
			plt.clf()
		elif iend == 0:
			plt.clf()
			return
		else:
			f, axarr = plt.subplots(1,iend)
			for i in range(go*(j),((j)*go)+iend): 
				im = axarr[i-(go*j)].imshow(image_data[i],cmap='gray')
				axarr[i-(go*(j))].set_title(gals[i])
			f.subplots_adjust(right=0.8)
			cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
			f.colorbar(im,cax = cbar_ax)
			f.savefig(os.path.join('Pictures',(gals[go*(j)]+".png")))
			plt.clf()

	#-----Saves Graphs and Data To The Directory-----# #saves all images in .png files

def GraphMaker(A_v,gals,majAxis):

	if(len(gals)>2):
		go = 2
		iend = go
		sz1 = (int(len(gals))//go)+1
		sz2 = (int(len(gals))-(go*(sz1-1)))
	else:
		go = len(gals)
		iend = go
		sz1 = (int(len(gals))//go)
		sz2 = (int(len(gals))-(go*(sz1-1)))
	for j in range(0,sz1):
		if j==sz1-1:
			iend = sz2
		if iend == 1:
			plt.clf()
			plt.figure(1)
			plt.plot(x,A_v[len(gals)-1][:,0], color = "blue", marker = ".", label = "North")
			plt.plot(x, A_v[len(gals)-1][:,1], color = "red", marker = ".", label = "East")
			plt.plot(x, A_v[len(gals)-1][:,2], color = "green", marker = ".", label = "South")
			plt.plot(x, A_v[len(gals)-1][:,3], color = "black", marker = ".", label = "West")
			plt.axvline(x=majAxis[j])
			plt.xlabel("Arcminutes from Center of Galaxy")
			plt.ylabel("A_v Value")
			plt.legend(loc='center right', shadow=True)
			plt.suptitle("A_v Values by Arcminute")
			plt.title(gals[len(gals)-1])
			plt.savefig(os.path.join('Graphs',(gals[len(gals)-1]+" Graph.png")))
			plt.clf()
		elif iend == 0:
			plt.clf()
			return
		else:
			f, axarr = plt.subplots(nrows = 1,ncols = iend, sharey = True, sharex = True,figsize = (20,10))
			f.text(.5,.04, 'Arcminutes From Center of Galaxy',ha='center',fontsize = 20)
			f.text(.08,.5, 'A_V Value',va='center', rotation='vertical',fontsize = 20)
			for i in range(go*(j),((j)*go)+iend): 
				no, = axarr[i-(go*j)].plot(x, A_v[i][:,0], color = "blue", marker = ".", label = "North")
				ea, = axarr[i-(go*j)].plot(x, A_v[i][:,1], color = "red", marker = ".", label = "East")
				so, = axarr[i-(go*j)].plot(x, A_v[i][:,2], color = "green", marker = ".", label = "South")
				we, = axarr[i-(go*j)].plot(x, A_v[i][:,3], color = "black", marker = ".", label = "West")
				axarr[i-(go*j)].axvline(x=majAxis[i])
				axarr[i-(go*(j))].set_title(gals[i], fontsize = 20)
			plt.figlegend((no,ea,so,we),("North","East","South","West"),loc='center right', shadow=True, prop={'size':20})
			plt.suptitle("A_v Values by Arcminute", fontsize = 20)
			f.savefig(os.path.join('Graphs',(gals[go*(j)]+" Graph.png")))
			plt.clf()

	#-----Saves Graphs and Data To The Directory-----# #saves all images in .png files

def getAxis(name,link,majAxis,minAxis):
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
	#-------Get Velocities-----#
	# velocities = soup.find_all('pre')[5]
	# Helio = list(velocities.children)[2]
	# VGS = list(velocities.children)[16]
	# Helio = Helio.lstrip('\n')
	# VGS = VGS.lstrip('\n')
	# Hvals = [int(s) for s in Helio.split() if s.isdigit()]
	# VGSVals = [int(s) for s in VGS.split() if s.isdigit()]
	#-----End Get Velocities-----#
	#-----Get Diameters-----#
	diameters = soup.find_all('table')[22]
	diameters = diameters.find_all('tr')[2]
	major = diameters.find_all('td')[1].get_text()
	minor = diameters.find_all('td')[2].get_text()
	#-----End Get Diameters-----#
	write_file = 'Data.csv'
	fix = False
	fix2 = False
	if(major != "..."):
		major = float(major)/60
		majAxis.append(major)
	else:
		major = "None"
		fix = True
		majAxis.append(None)
	if(minor != "..."):
		minor = float(minor)/60
		minAxis.append(minor)
	else:
		minor = "None"
		fix2 = True
		minAxis.append(None)
	with open(write_file, 'a') as output:
		if(fix and fix2):
			output.write(name + ',' + major + ',' + minor + '\n')	
		elif(fix == True and fix2 == False):
			output.write(name + ',' + major + ',' + '%.3f' %minor + '\n')
		elif(fix == False and fix2 == True):
			output.write(name + ',' + '%.3f' %major + ',' + minor + '\n')
		else: output.write(name + ',' + '%.3f' %major + ',' + '%.3f' %minor + '\n')
	
from astropy.coordinates import name_resolve

#-----SETUP-----#
c3 = None
link = "https://ned.ipac.caltech.edu/cgi-bin/objsearch?"
gals = []
start_coord = []
print("\nWelcome to A_v Calculator!\n")
print("Created by: Tate Walker for Dr. Peter Brown at Texas A&M University\n")
can_read = False
while can_read == False:
	choice = input("Enter [1] to enter galaxies by hand. Enter [2] to import a .txt file of names. Enter [q] to quit.\n")
	if choice == '1':
		galaxies = input("Enter galaxies separated by commas: Ex. M82, M83\n")
		for x in galaxies.split(','):
			gals.append(x.strip())
		can_read = True	
	elif choice == '2':
		file = input("What is the name of the file? Ex. galaxies.txt\n")
		with open(file) as inp:
			gals = inp.read().splitlines()
		can_read = True
		choice == '2'
	elif choice == 'q':sys.exit()
	else: print("Please enter either [1], [2], or [q]\n\n")

c1 = input("Do you want to get A_v values? [y] [n] \n") #option to get values
if c1 == 'y':c3 = input("Do you want to graph these values? [y] [n] \n") #option to graph
c2 = input("Do you want to get pictures of each galaxy? [y] [n] \n") #option to get pictures

if c1 == 'y':
	dam = input("How many arcminutes?\n")
	dam = int(dam)

elif c1 and c2 == 'n':
	print("Those are all the options, please come back if you change your mind.")
	sys.exit()

for i in range(0,len(gals)):
	tcoord=SkyCoord.from_name(gals[i],frame ='icrs') #gets coordinate from name given and stores in temporary SkyCoord
	start_coord.append(tcoord) #puts temporary SkyCoord in a list
	
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
A_v = []
majAxis = []
minAxis = []
ra = Angle(start_coord[0].ra.hour,unit = u.hour) #gets radius of 1st coordinate as an angle (needed for things to work)
dec = start_coord[0].dec #dont need an angle for some reason but it works

appender = 'w' #lets us overwrite a file or make a new one
nme = gals[0]

import itertools
import threading
import time
import sys

done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print(chr(27) + "[2J")
    sys.stdout.write('\rDone!')

print(chr(27) + "[2J")
threader = threading.Thread(target=animate)
threader.start()
if c1 == 'y':A_v.append(tableFill(dam,ra,dec,appender,nme)) #runs the main functionality and returns the data of a galaxy
if c2 == 'y':grabImage(ra,dec) #gets image data and stores in list
appender = 'a' #lets us append a file instead of overwriting
for i in range(1,len(start_coord)):
	nme = gals[i]
	ra = Angle(start_coord[i].ra.hour,unit = u.hour)
	dec = start_coord[i].dec
	if c1 == 'y':A_v.append(tableFill(dam,ra,dec,appender,nme))
	if c2 == 'y':grabImage(ra,dec)
if c2 == 'y':PicSaver(image_data,gals) #saves all images in .png files, don't mess with this
if c3 == 'y':
	x = np.arange(dam+1) #creates array of size dam+1 to store values
	A_v = np.array(A_v) #numpy array needed to graph
	write_file = 'Data.csv'
	with open(write_file, 'w') as output:
		output.write("Name, Apparent Major Axis (arcmin), Apparent Minor Axis (arcmin)\n")
	for i in range(0,len(gals)):
		nme = gals[i]
		getAxis(nme,link,majAxis,minAxis)
	GraphMaker(A_v,gals,majAxis)
done = True
time.sleep(3)
print(chr(27) + "[2J")
print("All pictures and graphs are saved in the project directory if selected. The A_v values are stored in the .csv file if calculated\n")
print("Thank you for using this program!\n")