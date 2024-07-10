"""
7/30/2023
@authors: Thomas Masha, Stefan Salaices
"""

import csv

SWIFTNames = []
SWIFTTypes = []

with open("AllSwiftSupernovae.csv", newline="") as csvFile:
    
    reader = csv.reader(csvFile)

    for row in reader: # row is a list containing [name, type, ra, dec]
        
        SWIFTNames.append(row[0].replace(" ","").replace("-","").upper())

# parallel lists for necessary TNS data
TNSPrefixes = []
TNSNames = []
TNSTypes = []

with open("tns_public_objects.csv", newline="", encoding="utf8") as csvFile2:
    
    reader = csv.reader(csvFile2)

    next(reader)
    next(reader)

    for row in reader:
 
        if row[1] != "" and row[2] != "":
            TNSNames.append(row[1] + row[2])
        else:
            TNSNames.append('not found')
        
        if row[7] != "":
            TNSTypes.append(row[7])
        else:
            TNSTypes.append('not found')

for i in range(len(SWIFTNames)):

    if SWIFTNames[i] in TNSNames:

        index = TNSNames.index(SWIFTNames[i])
        SWIFTTypes.append(TNSTypes[index])

    #else:
        #if internal names
        #for loop names after applying upper and replace stuff
        
    else:
        SWIFTTypes.append("not found")

for i in range(len(SWIFTNames)):
    print(f"{SWIFTNames[i]} is of type {SWIFTTypes[i]}")