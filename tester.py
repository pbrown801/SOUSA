#tester.py

from astropy import units as u
from astropy import coordinates

from astroquery.irsa_dust import IrsaDust
from astroquery.ned import Ned
from astropy.coordinates import Angle,ICRS,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
import math
import os.path
import sys

import requests
link = "https://ned.ipac.caltech.edu/cgi-bin/objsearch?"

inputs = {'objname': "anon",
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
soup = soup.find("a", attrs={'name':'BasicData_0'})
soup = soup.next_sibling.next_sibling.next_sibling.find("pre")
redshift = list(soup.children)[1]
redshift = str(redshift).split(">",1)[1]
redshift = redshift.split("<",1)[0]
print(redshift)
	
# redshift = redshift.find_all('pre')[0]
# redshift = list(redshift.children)[1]
# redshift = str(redshift).split(">",1)[1]
# redshift = redshift.split("<",1)[0]


