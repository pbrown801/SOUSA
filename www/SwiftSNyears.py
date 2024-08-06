"""
Stefan Salaices, Kriti 

The purpose of this program is to sift through a list 
of objects and clean it up. We removed hashtags, duplicates,
looked for and assigned years for each object type.

modified for csv by Dr. Brown
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib



inputcsv='TrimmedAllSwiftSNlist.csv'
swift= pd.read_csv(inputcsv,on_bad_lines='warn',delimiter=',')


#with open('snlist.txt','r') as file:
#    snlist = file.readlines()

#strippedlines = [sn.strip() for sn in snlist] #removes spaces on each line

years = [2005,2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023,2024]
shortyears = ['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24']
gapyears = ['2005', '  ', '  ', '  ', '  ', '2010', '  ', '  ', '  ', '  ', '2015', '  ', '  ', '  ', '  ', '2020', '  ', '  ', '  ','2024']
years = [str(year) for year in years]
newlist = [] #empty list we'll add objects that meet the criteria

if 'year' not in swift:
    swift['year']=np.nan

for name in swift.SNname: #go through doc
    print(name)
    if any(substring in name for substring in years):
       
        for yearstep in years:
            if yearstep in name:
                 
                swift.year[swift['SNname'] == name] = yearstep #adding to the list
                print(yearstep, " added based on year")
            else:
                continue

    #special cases in which full years do not appear
    elif "ASASSN-" in name:
        year = name[7:9] #extract 2 digits of year "16, etc"
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        print(year, "ASASSN added")
        continue

    elif "Gaia" in name:
        year = name[4:6]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        print(year, "Gaia added")
        continue

    elif "OGLE" in name:
        year = name[4:6]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        print(year, "OGLE added")
        continue

    elif "LSQ" in name:
        year = name[3:5]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        print(year, "LSQ added")
        continue

    elif "ZTF" in name:
        year = name[3:5]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        continue

    elif "iPTF" in name:
        year = name[4:6]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        print("does iptf ever get caught?")
        continue

    elif "PTF" in name:
        year = name[3:5]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        continue

    elif "CSS" in name:
        year = name[3:5]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        continue

    elif "PSN" in name:
        print(f"{name} needs a year")
        continue

    elif "PS1-" in name:
        year = name[4:6]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        continue

    elif "PS" in name:
        year = name[2:4]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        continue

    elif "DES" in name:
        year = name[3:5]
        year = int(year) + 2000
        swift.year[swift['SNname'] == name] = year
        continue

    else:
        print(f"{name} did not process")



sortedswift=swift.sort_values(['year','SNname'], ascending=[False,False])

print(sortedswift)


#print(f"Removed {len(newlist) - len(cleanedlist)} duplicates.")

trimmedswift=sortedswift.drop_duplicates()

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

#extracting years and graphing
yearcountlist = []
for year in years:
    yearcount = 0
    for Swiftyear in trimmedswift['year']:
        if Swiftyear == str(year):
            yearcount += 1
    yearcountlist.append(yearcount)

plt.figure(figsize=(12, 8))
plt.bar(shortyears, yearcountlist, color="slateblue")
#plt.title("Swift Observations")
plt.xlabel("Year")
plt.ylabel("Swift Supernovae per Year")
#plt.legend(loc="upper left")

plt.show()
matplotlib.pyplot.savefig('SwiftSNyears.png')

print(trimmedswift.SNname[trimmedswift.year == '2020'])
trimmedswift.to_csv('Sorted'+inputcsv, index= False)
