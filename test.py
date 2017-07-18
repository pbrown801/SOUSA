import requests
link = "https://ned.ipac.caltech.edu/cgi-bin/objsearch?"
name = 'm82'
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

#-----Get Diameters-----#

#-----SETUP-----#

gals = []