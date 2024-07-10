
#modified from newcsv.py from Hazem and Thomas

import pandas as pd
import csv, json


SwiftPTFnames, SwiftPTFiaunames, SwiftPTFaltnames, SwiftPTFtypes, SwiftPTFredshifts, SwiftPTFra, SwiftPTFdec = [], [], [], [], [], [], []

Swiftnames, Swifttypes, Swiftra, Swiftdec = [], [], [], []


# get Swift targets
# this list is from Stefan's CombinedAllSwiftSupernovae.py code
# which pulled all possible supernovae (ie starting with SN or PTF or ASASSN, etc)
# We aren't sure which of the PTF objects are supernovae until we compare with the published lists

with open('AllSwiftSupernovae.csv', 'r') as allswiftlist:
    for line in allswiftlist:
        line = line.split(',')
        Swiftnames.append(line[0])
        Swifttypes.append(line[1])
        Swiftra.append(line[2])
        Swiftdec.append(line[3])

checked_names = set()


# Read PTF_CClist.txt
with open('PTF_CClist.txt', 'r') as ptflist:
    for line in ptflist:
        #line = line.split()
        linename = line[0:9]
        linename = linename.strip()
        print(linename)
        if linename.lower() in checked_names:
            continue
        for nova in Swiftnames:

            if nova.lower() == linename.lower() and linename.lower() not in checked_names:
                iauname=line[39:46]
                if iauname[0] == ' ':
                    SwiftPTFnames.append(line[0:9].strip())
                    SwiftPTFaltnames.append(' ')
                else:
                    SwiftPTFnames.append('SN'+line[39:46].strip())
                    SwiftPTFaltnames.append(line[0:9].strip())
                if line[10:11] == 'SN':
                    SwiftPTFtypes.append(line[12:19].strip())
                else:
                    SwiftPTFtypes.append(line[10:19].strip())
                SwiftPTFredshifts.append(line[20:28].strip())
                SwiftPTFra.append(line[47:60].strip())
                SwiftPTFdec.append(line[61:75].strip())
                print(f'Added {line[0:9]} with type {line[10:19]} and ra {line[47:60]}.')
                checked_names.add(linename.lower())



with open('iPTFlist.txt', 'r') as iptflist:
    for line in iptflist:
        line = line.split()
        curr = 'iPTF' + line[0].replace(" ","")
        if curr in checked_names:
            continue
        #print('in iPTFlist ',curr)
        for nova in Swiftnames:
            if nova.replace(" ","").lower() == curr.lower() and curr not in checked_names:
                SwiftPTFnames.append(curr)
                SwiftPTFaltnames.append(' ')
                SwiftPTFtypes.append('Ia')
                SwiftPTFredshifts.append('')
                SwiftPTFra.append('')
                SwiftPTFdec.append('')
                print(curr, "is added to Swift list")
                checked_names.add(curr)
        checked_names.add(curr)

# PTF list csv

with open('ptfs.csv', 'r') as ptfcsv:
    reader = csv.reader(ptfcsv)
    for row in reader:
        if row[1] != 'NULL':
            if 'SN' + row[1] in Swiftnames:
                SwiftPTFnames.append('SN' + row[1])
                SwiftPTFaltnames.append(' ')
                SwiftPTFtypes.append("Ia")
                SwiftPTFredshifts.append(row[-2])
                SwiftPTFra.append(row[2])
                SwiftPTFdec.append(row[3])
                print(f'SN{row[1]} found.')
                continue
        if row[0] in Swiftnames:
            SwiftPTFnames.append(row[0])
            SwiftPTFaltnames.append(' ')
            SwiftPTFtypes.append("Ia")
            SwiftPTFredshifts.append(row[-2])
            SwiftPTFra.append(row[2])
            SwiftPTFdec.append(row[3])
            print(f'{row[0]} found.')

        if 'SN' + row[1] in Swiftnames:
            SwiftPTFnames.append('SN' + row[1])
            SwiftPTFaltnames.append(' ')
            SwiftPTFtypes.append("Ia")
            SwiftPTFredshifts.append(row[-2])
            SwiftPTFra.append(row[2])
            SwiftPTFdec.append(row[3])
            print(f'SN{row[1]} found.')
                
        if row[0] in Swiftnames:
            SwiftPTFnames.append(row[0])
            SwiftPTFaltnames.append(' ')
            SwiftPTFtypes.append("Ia")
            SwiftPTFredshifts.append(row[-2])
            SwiftPTFra.append(row[2])
            SwiftPTFdec.append(row[3])
            print(f'{row[0]} found.')




# load all the json data as lowercased
with open('altnames.json', 'r') as json_file:
    json_data = json.load(json_file)

altnames = {}
for key, value in json_data.items():
    curr = []
    for item in value:
        item = item.strip()
        if item[-1] == ',': item = item[:-1]
        curr.append(item.lower())
    altnames[key] = curr



# search for cross-matches and missing redshifts
changed = 0
prefixes = ['ztf', 'ptf', 'iptf', 'atlas', 'dlt', 'gaia', 'asassn']
for i, name in enumerate(SwiftPTFnames):
    name = name.lower()
    # skip any nova that does not have these prefixes
    if not any(name.startswith(prefix) for prefix in prefixes): continue
    # check all novae in Transient Name Server data for cross-matches
    for item in altnames:
        # if a SN match is found, change the name to the SN name
        if name.lower().strip() in altnames[item]:
            if 'PTF' in name:
                print(f'Cross-match successful: {names[i]} was changed to {item}.')
            SwiftPTFnames[i] = item
            changed += 1
            break

# reformat SN supernovae so they have the correct(?) casing
print(f'\n{changed} cross-matches found. Formatting...')
for i, name in enumerate(SwiftPTFnames):
    if name[:2].lower() == 'sn':
        SwiftPTFnames[i] = 'SN' + name[2:].lower()

# search for missing redshifts and other data
print('Searching for missing redshifts...')
names_shifts = {}
names_types = {}
ras = {}
decs = {}
with open('tns.csv', 'r') as tnscsv:
    reader = csv.reader(tnscsv)
    next(reader, None)
    next(reader, None)
    for row in reader:
        # print(f'SN{row[2]} -> {row[5]}?')
        currname = 'SN' + row[2]
        if isinstance(row[7], str) and row[7].strip():
            names_types[currname] = row[7].split()[-1]
        names_shifts[currname] = row[5]
        ras[currname] = row[3]
        decs[currname] = row[4]

for i, name in enumerate(SwiftPTFnames):
    
    if SwiftPTFtypes[i] == '':
        try:
            types[i] = SwiftPTFnames_types[name]
        except:
            do_nothing = 1


    if SwiftPTFredshifts[i] == '':
        try:
            SwiftPTFredshifts[i] = names_shifts[name]
            # print(f"{name}'s redshift was updated to {names_shifts[name]}.")
        except:
            do_nothing = 1
            # print(f'No redshift found for {name}.')
        
    if SwiftPTFra[i] == '':
        try:
            SwiftPTFra[i] = ras[name]
        except:
            do_nothing = 1

    if SwiftPTFdec[i] == '':
            # print('not found')
        try:
            SwiftPTFdec[i] = decs[name]
        except:
            do_nothing = 1
            # print('not found')

# reformat types
print('Reformatting types...')
seen = []
for i, t in enumerate(SwiftPTFtypes):
    t.strip()
    if t.startswith('SN ') or t.startswith('SL '):
        t = t[3:]
    if '[02cx-like]' in t:
        t = 'Iax'
    elif '91T' in t:
        t = 'Ia-91T-like'
    elif 'Ibc' in t:
        t = 'Ib/c'

    
    SwiftPTFtypes[i] = t.strip()

# create df, write to csv
print('Creating dataframe...')
df = pd.DataFrame(list(zip(SwiftPTFnames, SwiftPTFtypes, SwiftPTFredshifts, SwiftPTFaltnames, SwiftPTFra, SwiftPTFdec)), columns = ['name', 'type', 'redshift', 'OtherName', 'right ascension', 'declination'])

print(df)

#print(df[:,'SwiftPTFra'])

print ('Dropping duplicates...')
df.drop_duplicates()

print('Writing to SwiftPTFdatabase.csv...')
df.to_csv('SwiftPTFdatabase.csv', index=False)

print(f'All done! {changed} cross-matches were found.')

