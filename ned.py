#query coordinates
import astropy.units as u
from astropy import coordinates

from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle

import math

def timeFix(s,m,h):
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

def unsureCoord(dam,ra,dec):
	ds = dam*4 #change in real seconds for radius
	dec = dec.arcminute+dam
	decl = Angle(dec,u.arcminute)
	ds/=math.cos(math.radians(decl.degree))

	h = ra.hms.h
	m = ra.hms.m
	s = (ra.hms.s)+ds
	(s,m,h) = timeFix(s,m,h) #fix time coordinates

	rad = Angle((h,m,s), unit = u.hour) #gets in new format

	print("Radius after 20 arcminutes:"), 
	print(rad.to_string(unit=u.hour))
	print("Declination after 20 arcminutes:"),
	print(decl.to_string(unit=u.degree))

	#resetting to original format
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)

	#creating coordinates from radius and declination
	coord = rad.to_string()+" +"+decl.to_string()
	print("New coord:"),
	print(coord)
	return coord;

def fourCoord(dam,ra,dec):
	ds = dam*4

	#e
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h)
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	coord[1] = rad.to_string()+" +"+dec.to_string()

	#n
	decli = dec.arcminute+dam
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	coord[0] = ra.to_string()+" +"+decl.to_string()
	
	#w
	ds=ds*(-1)
	ds/=math.cos(math.radians(dec.degree))
	h = ra.hms.h
	m = ra.hms.m
	s = ra.hms.s+ds
	(s,m,h) = timeFix(s,m,h)
	rad = Angle((h,m,s), unit = u.hour)
	rad = Angle(rad.to_string(unit=u.hour),u.hour)
	coord[3] = rad.to_string()+" +"+dec.to_string()

	#s
	decli = dec.arcminute-dam
	decl = Angle(decli,u.arcminute)
	decl = Angle(decl.to_string(unit=u.degree),u.degree)
	coord[2] = ra.to_string()+" +"+decl.to_string()
	
	#print(coord)
	return coord;

#creating angles and printing
ra = Angle('09h55m52.7s',u.hour)
dec = Angle('69d40m46s',u.degree)
print("Original radius: %s" %(ra.to_string()))
print("Original declination: %s" %(dec.to_string()))

z = 0
dam = 60 #20 arcminutes
#dtsquared = (pow(dalpha*math.cos(decl),2)+pow(ddecl,2))

A_v = []
curVal = [None] *4 #n = 0, e = 1, s = 2, w = 3
coord = [None] *4 #n = 0, e = 1, s = 2, w = 3

#get values for each arcminute
for j in range(0,dam+1):
	fourCoord(j, ra, dec)
	for i in range(0,4):
		C = coordinates.SkyCoord(coord[i])
		table = IrsaDust.get_extinction_table(C.fk5)
		curVal[i] = (table['A_SandF'][2])
		curVal = curVal[:]
#	print(j,": ",coord)
	A_v.append(curVal)

#print values for each arcminute
for sublst in A_v:
	print(z),
	print("Arcminutes: "),
	for item in sublst:
		print(item),
	print("")
	z+=1

import matplotlib.pyplot as plt
import numpy as np
x = np.arange(dam+1)
A_v = np.array(A_v)
plt.plot(x,A_v[:,0], color = "blue", marker = ".", label = "North")
plt.plot(x, A_v[:,1], color = "red", marker = ".", label = "East")
plt.plot(x, A_v[:,2], color = "green", marker = ".", label = "South")
plt.plot(x, A_v[:,3], color = "black", marker = ".", label = "West")
plt.title("A_v Values by Arcminute")
plt.xlabel("Arcminutes from Center of Star")
plt.ylabel("A_v Value")
plt.legend(loc='lower left', shadow=True)
plt.show()