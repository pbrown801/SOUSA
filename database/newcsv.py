import pandas as pd
import csv, json

# append the novae from found.json (swifts)
f = open('found.json')
found = json.load(f)
f.close()

names, types, redshifts, ra, dec = [], [], [], [], []
for i, j in found.items():
    names.append(i)
    types.append(j)
    redshifts.append('')
    ra.append('')
    dec.append('')
    # print(f'Added {i} with type {j}.')

# append the updated.csv names, types
with open('updated.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        if '_dup' in row[0]: continue
        names.append(row[0])
        types.append(row[1])
        redshifts.append(row[2])
        ra.append('')
        dec.append('')
        # print(f'Added {row[0]} with type {row[1]} and redshift {row[2]}.')


# need to ensure that the PTFs we add are in the swift list too
swifts = []
with open('NewSwiftSNweblist.csv', 'r') as swiftfile:
    reader = csv.reader(swiftfile)
    for row in reader:
        swifts.append(row[0].lower())
        # print(row[0])

                
# get PTFs
with open('PTF_CClist.txt', 'r') as ptflist:
    for line in ptflist:
        line = line.split()
        for nova in swifts:
            if nova == line[0].lower():
                # print(f'{nova} = {line[0]}')
                names.append(line[0])
                types.append(line[1])
                redshifts.append(line[2])
                ra.append(line[5] + ' ' + line[6] + ' ' + line[7])
                dec.append(line[8] + ' ' + line[9] + ' ' + line[10])
                # print(f'Added {line[0]} with type {line[1]} and redshift {line[2]}.')


already_checked = []
with open('iPTFlist.txt', 'r') as iptflist:
    for line in iptflist:
        line = line.split()
        for nova in swifts:
            curr = 'iPTF' + line[0]
            if curr in already_checked:
                continue
            already_checked.append(curr)
            for nova in swifts:
                if nova == curr.lower():
                    names.append(curr)
                    types.append('Ia')
                    redshifts.append('')
                    ra.append('')
                    dec.append('')
                    # print(f'{nova} = {curr}')


# PTF list csv

with open('ptfs.csv', 'r') as ptfcsv:
    reader = csv.reader(ptfcsv)
    for row in reader:
        if row[1] != 'NULL':
            if 'SN' + row[1] in swifts:
                names.append('SN' + row[1])
                types.append(row[-3])
                redshifts.append(row[-2])
                ra.append(row[2])
                dec.append(row[3])
                print(f'SN{row[1]} found.')
                continue
        if row[0].lower() in swifts:
            names.append(row[0])
            types.append(row[-3])
            redshifts.append(row[-2])
            ra.append(row[2])
            dec.append(row[3])
            print(f'{row[0]} found.')


# haz's list

with open('outfile1.txt', 'r') as outfile1:
    for line in outfile1:
        names.append(line)
        types.append('')
        redshifts.append('')
        ra.append('')
        dec.append('')


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
for i, name in enumerate(names):
    name = name.lower()
    # skip any nova that does not have these prefixes
    if not any(name.startswith(prefix) for prefix in prefixes): continue
    # check all novae in Transient Name Server data for cross-matches
    for item in altnames:
        # if a SN match is found, change the name to the SN name
        if name.lower().strip() in altnames[item]:
            if 'PTF' in name:
                print(f'Cross-match successful: {names[i]} was changed to {item}.')
            names[i] = item
            changed += 1
            break

# reformat SN supernovae so they have the correct(?) casing
print(f'\n{changed} cross-matches found. Formatting...')
for i, name in enumerate(names):
    if name[:2].lower() == 'sn':
        names[i] = 'SN' + name[2:].lower()

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

for i, name in enumerate(names):
    
    if types[i] == '':
        try:
            types[i] = names_types[name]
        except:
            do_nothing = 1


    if redshifts[i] == '':
        try:
            redshifts[i] = names_shifts[name]
            # print(f"{name}'s redshift was updated to {names_shifts[name]}.")
        except:
            do_nothing = 1
            # print(f'No redshift found for {name}.')
        
    if ra[i] == '':
        try:
            ra[i] = ras[name]
        except:
            do_nothing = 1

    if dec[i] == '':
            # print('not found')
        try:
            dec[i] = decs[name]
        except:
            do_nothing = 1
            # print('not found')

# reformat types
print('Reformatting types...')
seen = []
for i, t in enumerate(types):
    t.strip()
    if t.startswith('SN ') or t.startswith('SL '):
        t = t[3:]
    if '[02cx-like]' in t:
        t = 'Iax'
    elif '91T' in t:
        t = 'Ia-91T-like'
    elif 'Ibc' in t:
        t = 'Ib/c'

    
    types[i] = t.strip()

# create df, write to csv
print('Creating dataframe...')
df = pd.DataFrame(list(zip(names, types, redshifts, ra, dec)), columns = ['name', 'type', 'redshift', 'right ascension', 'declination'])

print(df)

print ('Dropping duplicates...')
df.drop_duplicates()

print('Writing to newdatabase.csv...')
df.to_csv('newdatabase.csv', index=False)

print(f'All done! {changed} cross-matches were found.')

