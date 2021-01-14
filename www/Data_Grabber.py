# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:14:39 2020

@author: Alexander Crabtree
""" 
import requests
import json
import pandas as pd #for dataframes
import numpy as np
import math
import sys
import itertools
import threading
import time
import astropy.units as u
from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError



def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print(chr(27) + "[2J")
    sys.stdout.write('\rDone!')

def getLink(name):
    
    try:
        link = "http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?"
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
				'list_limit':'10',
				'img_stamp': 'YES'}
        page = requests.get(link, params = inputs)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except requests.ConnectionError:
        soup = ''
        return soup

def scrapeValues(soup):
	#----------Get Velocities----------#
    try:
        soup = soup.find("a", attrs={'name':'DerivedValues_0'})
        velocities = soup.next_sibling.next_sibling.next_sibling.find("pre")
        Helio = list(velocities.children)[2]
        VGS = list(velocities.children)[16]
        Helio = Helio.lstrip('\n')
        VGS = VGS.lstrip('\n')
        Hvals = [int(s) for s in Helio.split() if s.isdigit()]
        VGSVals = [int(s) for s in VGS.split() if s.isdigit()]
        vels = [Hvals[0],Hvals[1],VGSVals[0],VGSVals[1]]
        return vels
    except: 
        vels = ['','','','']
        return vels

def get_coords(gals):
    """
        Takes list of galaxies and looks up their coordinates by name.
        If no name found: warn, skip, remove galaxy from list

        Returns:
            gals: list of galaxies minus those that weren't found
            start_coord: list of coordinates corresponding to center of galaxies in 'gals'
    """
    start_coord = []
    #bar = FillingCirclesBar('Loading galaxies', max = len(gals))
    try:
        tempCoord = SkyCoord.from_name(str(gals), frame = 'icrs')
        start_coord= tempCoord
            #bar.next()
    except NameResolveError:
        #if gals != str(''):
            #print('\nSkipping',gals,'because it couldn\'t be found.')
            #start_coord= ''
        #else:
            start_coord= ''
    #bar.finish()
    return(start_coord)

def coord_breakup(coord):
    """
        Breaks up a coordinate into its components
    """
    if coord != '':
        ra = Angle(coord.ra.hour,unit = u.hour)
        dec = coord.dec
        return(ra, dec)
    else:
         ra = ''
         dec = ''
         return(ra, dec)


def Redshift(soup):

    try:
        soup = soup.find("a", attrs={'name':'BasicData_0'})
        soup = soup.next_sibling.next_sibling.next_sibling.find("pre")
        redshift = list(soup.children)[0]
        # print(redshift)
        redshift = str(redshift).split("Redshift",1)[1]
        # print(redshift)
        redshift = redshift.split(":",1)[1]
        redshift = redshift.split(" +",1)[0].strip(' ')
        return(redshift)
    except:
        redshift = ''
        return redshift
   

def Morphology(soup):
    
    try:
        soup = soup.find("a", attrs={'name':'BasicData_0'})
        morphology = soup.next_sibling.next_sibling.next_sibling.find("pre")
        morphology = list(morphology.children)[2]
        morphology = (morphology.split(": ",4)[4]).rstrip()
        return morphology
    except:
        morphology = ''
        return morphology


def LatLong(soup):
    
    try:
        soup = soup.find("a", attrs={'name':'Positions_0'})
        coords = soup.next_sibling.next_sibling.find("pre")
        coords = list(coords.children)[4]
        coords = (coords.split("Galactic ",1)[1]).lstrip()
        long, lat = str(coords.split()[0]), str(coords.split()[1])
 
        return long, lat
    except:
        long, lat= '',''
        return long, lat  

        
def getAVbest(inputcoordinates):
    '''
    Coordinates are input as a single string. Output is the recommended Av value for MW reddening, error, and reference
    '''
    
    #inputcoordinates = sys.argv[1]
    testCoords = SkyCoord(inputcoordinates,frame='fk5')

    #print('\n-----\nReading input files...')
    inFile = 'Brown_Walker_table_1.dat'
    inTable = pd.read_csv(inFile,header=None,delimiter=' ')
    ra = Angle(inTable.iloc[:,1])
    dec = Angle(inTable.iloc[:,2])
    sourceCoords = SkyCoord(ra,dec,frame='fk5')
    
    #print('Calculating separation from table coordinates')
    separations = testCoords.separation(sourceCoords).arcminute
    # compare to the distances in the table
    within = np.less(separations,inTable.iloc[:,3])
    
    # Are any of the input coordinates within the tabulated distance 
    # of the coordinates in the table?
    correctedAV = np.where(within,inTable.iloc[:,4],None) #get calculated value
    fix=any(within)
    #print('fix?',fix)
    
    if fix:
        AV = next((item for item in correctedAV if item is not None),None)
        correctedAVerr = np.where(within,inTable.iloc[:,5],None) #get calculated val
        newAVerr = next((item for item in correctedAVerr if item is not None),None)
        AVerr = math.sqrt((newAVerr)**2+(AV*0.1)**2)
        sources=np.where(within,inTable.iloc[:,6],None)
        source = next((item for item in sources if item is not None),None)+",S_F_2011"
    if not fix:
        AVtable = IrsaDust.get_extinction_table(testCoords,show_progress = False)
        AV=AVtable['A_SandF'][2]
        AVerr = AV*0.1
        source = 'S_F_2011'

    #print(AV, AVerr, source)
    return (AV, AVerr, source);

# create a formatted string of the Python JSON object-------------------------
def jprint(obj):
    
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
done = False
print(chr(27) + "[2J")
threader = threading.Thread(target=animate)
threader.start()

#read csv file----------------------------------------------------------------
swift= pd.read_csv('NewSwiftSNweblist.csv')
swift= swift.replace({r'anon',r'Anon',r'AnonHost'},np.nan, regex=True)
swift = swift.fillna('')

#requests astrocats catalog---------------------------------------------------
sn_data= requests.get("https://api.astrocats.space/catalog/ra+dec+host?first")
sn_catalog= sn_data.json()

#gathers host, ra, and dec data of SN-----------------------------------------
def SNHost(SNname):
    
    if SNname in sn_catalog:
        try:
            host_names= sn_catalog[SNname]['host']['value']
        except Exception:
            host_names= ''
    else:
        host_names= ''
    return host_names

def SNRa(SNname):
    
    if SNname in sn_catalog:
        try:
            snra= "'%s" % sn_catalog[SNname]['ra']['value']
        except Exception: 
            snra= ''
    else:
        snra= ''
    return snra

def SNDec(SNname):
    if SNname in sn_catalog:
        try:
            sndec= sn_catalog[SNname]['dec']['value']
        except Exception: #if no dec value input what is given for dec 
            sndec= ''
    else:
        sndec= ''
    return sndec
swift["HostName"]= swift.apply(lambda row: SNHost(SNname=row['SNname']), axis=1)
swift["SNra"]= swift.apply(lambda row: SNRa(SNname=row['SNname']), axis=1)
swift["SNdec"]= swift.apply(lambda row: SNDec(SNname=row['SNname']), axis=1)

#gathers AV data on SuperNovae------------------------------------------------
def GrabAVbest(Ra,Dec):
    if Ra is not str('') and Dec is not str(''):
        ra_fix, dec_fix = Ra, Dec
        ra_fix= ra_fix.replace("'", "")
        combined= SkyCoord(ra=ra_fix, dec=dec_fix, unit=(u.hour, u.deg)).to_string('hmsdms')

        try:
            AV,AVerr,source= getAVbest(combined)
        except Exception:
            AV,AVerr,source= '','',''
    else:
        AV,AVerr,source= '','',''
    return pd.Series({'AV': AV, 'AVerr': AVerr, 'AVsour': source})

avbest_data=['AV', 'AVerr', 'AVsour']
if sum(swift.columns.isin(avbest_data))!= 3:
    swiftAV= pd.DataFrame(swift.apply(lambda row: GrabAVbest(Ra=row['SNra'], Dec=row['SNdec']), axis=1 ))
    swift= pd.concat([swift,swiftAV], axis=1, sort=False)


#gathers data about host galaxy ---------------------------------------------
def AllHostData(HostName):
    if HostName is not str(''):
        ra,dec= coord_breakup(get_coords(HostName))
        gal_link=getLink(HostName)
    
        long, lat= LatLong(gal_link)
        red, morph= Redshift(gal_link), str(Morphology(gal_link))
        vels= scrapeValues(gal_link)
    else:
        ra, dec, long, lat, red, morph= '','','','','',''
        vels= ['','','','']
    return pd.Series({'HostRa':ra, 'HostDec':dec, 'Long':long, 'Lat':lat, \
                      'Redshift':red, 'Morphology':morph, 'V (Helio)':vels[0],\
                      'VError':vels[1], 'VGS':vels[2], 'VGSError':vels[3]})
        
hostdata_names= ["HostRa", "HostDec", "Long", "Lat", "Redshift", "Morphology", "V(Helio)", "VError", "VGS", "VGSError"]

if sum(swift.columns.isin(hostdata_names))!= 10:
    swiftHostData= pd.DataFrame(swift.apply(lambda row: AllHostData(row['HostName']), axis=1))
    swift= pd.concat([swift,swiftHostData], axis=1, sort=False)
    

#saves previous and new swift data to new csv---------------------------------
swift.to_csv('SwiftSNweblist.csv', index= False)

done= True
