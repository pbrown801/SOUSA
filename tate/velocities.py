import requests
import itertools
import threading
import time
import sys

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print(chr(27) + "[2J")
    sys.stdout.write('\rDone!')

def getVelocities(name,link):
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
	at = diameters.find('tr')
	print(at.get_text)
	diameters = diameters.find_all('tr')[0]
	major = diameters.find_all('td')[1].get_text()
	minor = diameters.find_all('td')[2].get_text()
	#-----End Get Diameters-----#
	write_file = 'Data.csv'
	with open(write_file, 'a') as output:
		output.write(name + ',' + str(Hvals[0]) + ',' + str(Hvals[1]) + ',' + str(VGSVals[0]) + ',' + str(VGSVals[1]) + ',' + major + ',' + minor + '\n')
	
#-----SETUP-----#
link = "https://ned.ipac.caltech.edu/cgi-bin/objsearch?"
gals = []
can_read = False
while can_read == False:
	choice = input("Enter [1] to enter galaxies by hand. Enter [2] to import a .txt file of names.\n")
	if choice == '1':
		galaxies = input("Enter galaxies separated by commas: Ex. M82, M83\n")
		for x in galaxies.split(','):
			gals.append(x.strip())
		can_read = True	
	elif choice == '2':
		file = input("What is the name of the file? Ex. galaxies.txt\n\n")
		with open(file) as inp:
			gals = inp.read().splitlines()
		can_read = True
	else:
		print("Please enter either [1] or [2]\n\n")

done = False
print(chr(27) + "[2J")
threader = threading.Thread(target=animate)
threader.start()

write_file = 'Data.csv'
with open(write_file, 'w') as output:
	output.write("Name, Heliocentric Velocity (km/s), Uncertainty (km/s), VGS Velocity (km/s), Uncertainty (km/s), Apparent Major Axis (arcsec), Apparent Minor Axis (arcsec)\n")

for i in range(0,len(gals)):
	name = gals[i]
	getVelocities(name,link)
done = True

