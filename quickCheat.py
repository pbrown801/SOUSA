import randomGal as rG


from astropy import units as u
from astropy import coordinates
from astroquery.ned import Ned
from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,ICRS,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
import math
import os.path
import sys

# import itertools
# import threading
# import time

# import requests
from astropy.coordinates import SkyCoord
from random import randint


ra = Angle((15, 9, 8.5), unit=u.hour) #creating right ascension angle
dec = Angle((67,13,21), unit=u.deg)

# tcoord = SkyCoord(ra, dec, frame = 'fk5')


ans = rG.tableFill(20,ra,dec)
print(ra)
print(dec)
print(ans)
