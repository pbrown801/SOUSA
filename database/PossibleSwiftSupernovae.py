"""
3/24/2023
@author: Stefan Salaices

This progam updates a megalist with all SWIFT observations since 2005 until the day the 
program is run then processes them and extracts all of the supernovae (some are not...) 
Currently collects name, type, RA, DEC, date, then writes to a file in addition to the list object.

To properly install the swifttools package with pip:

    pip install swifttools --user 

        the "--user" prevents access denied errors
        if you recieve a yellow text warning along the lines of "The script is installed in (some directory), which is not PATH", 
        follow these detailed instructions https://superuser.com/questions/1372793/the-script-is-installed-in-directory-which-is-not-path 

    for troubleshooting packages with pip, you can use the following commands:
    
        pip help //shows all commands
        pip list //shows all packages installed
        pip freeze > requirements.txt //pushes a list of all packages to a .txt file
        pip uninstall -r requirements.txt -y --user //uninstalls all installed packages with permissions
"""

from swifttools.swift_too import TOORequests
from datetime import date
import csv, itertools

years = []
MegaList = []
criteria = ["SN", "AT", "ZTF", "iPTF", "PTF", "ASASSN", "DLT"]
PossibleSwiftSupernovae = []
Imposters = []

for i in range(5, int(str(date.today())[2:4]) + 2): #gathers a list of years
    end = "-01-01 00:00:00"
    if i < 10:
        year = "200" + str(i) + end
    else:
        year = "20" + str(i) + end
    years.append(year)

print(years)

for i in range(len(years)): #chunks API calls into 1 years worth of data
    try:
        start_date = years[i]
        end_date = years[i+1]
    except: #chunks the last bit of data that isn't a full year
        start_date = years[len(years) - 1]
        end_date = str(date.today()) + "00:00:00"

    try:
        print(f"Retrieving... \n{start_date} --> {end_date}\n")
        toos = TOORequests(begin = start_date, end = end_date) #actual API call
        

        for too in toos: #get specific data from each object and write to csv
            too_source = too.source_name
            too_type = too.source_type	
            too_ra = too.ra
            too_dec = too.dec

            too_attributes = [too_source, too_type, too_ra, too_dec]

            MegaList.append(too_attributes) #add to list 

    except: #shouldn't ever happen... every comp sci major's famous last words
        print(f"Something went wrong! Skipping for now...\n")

MegaListClean = list(k for k,_ in itertools.groupby(MegaList))

print("Successfully Updated MegaList.csv!\nSearching for Supernova...\n")

for too in MegaListClean:
    
    name = str(too[0])
    desc = str(too[1])

    if "impost" in desc.lower(): #keeps track of imposters in case we want to know more later..
        Imposters.append(too)
        continue

    for criterion in criteria: #check for "ASASSN", "AT", "ZTF", "iPTF", "PTF", "SN", "DLT"
        if criterion.lower() in name.lower():
            if not (("bat" in name.lower()) or ("comet" in desc.lower())): #excludes BAT objects, comets 
                PossibleSwiftSupernovae.append(too)
                print(name)

#removes duplicates since SN and ASSASN will create duplicate entries from my loops.
PossibleSwiftSupernovaeClean = list(k for k,_ in itertools.groupby(PossibleSwiftSupernovae))

with open("PossibleSwiftSupernovae.csv", "w", newline = "", encoding = "utf-8") as wdata: #writing to another csv
    csvwriter = csv.writer(wdata)

    for i in range(len(PossibleSwiftSupernovaeClean)):
        csvwriter.writerow(PossibleSwiftSupernovaeClean[i])

print("Successfully Updated PossibleSwiftSupernovae.csv!")