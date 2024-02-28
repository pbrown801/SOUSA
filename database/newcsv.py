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
    print(f'Added {i} with type {j}.')

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
        print(f'Added {row[0]} with type {row[1]} and redshift {row[2]}.')


# need to ensure that the PTFs we add are in the swift list too
swifts = []
with open('NewSwiftSNweblist.csv', 'r') as swiftfile:
    reader = csv.reader(swiftfile)
    for row in reader:
        swifts.append(row[0])
        print(row[0])
# get PTFs
with open('PTF_CClist.txt', 'r') as ptflist:
    for line in ptflist:
        line = line.split()        
        if line[0] not in str(swifts): continue
        names.append(line[0])
        types.append(line[1])
        redshifts.append(line[2])
        ra.append('')
        dec.append('')
        print(f'Added {line[0]} with type {line[1]} and redshift {line[2]}.')

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
ras = {}
decs = {}
with open('tns.csv', 'r') as tnscsv:
    reader = csv.reader(tnscsv)
    next(reader, None)
    next(reader, None)
    for row in reader:
        print(f'SN{row[2]} -> {row[5]}?')
        currname = 'SN' + row[2]
        names_shifts[currname] = row[5]
        ras[currname] = row[3]
        decs[currname] = row[4]

for i, name in enumerate(names):
    if redshifts[i] == '':
        try:
            redshifts[i] = names_shifts[name]
            print(f"{name}'s redshift was updated to {names_shifts[name]}.")
        except:
            print(f'No redshift found for {name}.')
        try:
            ra[i] = ras[name]
        except:
            print('not found')
        try:
            dec[i] = decs[name]
        except:
            print('not found')

# reformat types
print('Reformatting types...')
seen = []
for i, t in enumerate(types):
    if t.startswith('SN '):
        types[i] = t[3:]
    if 'like' in t.lower():
        idxh = t.find('-')
        idxb = t.find('[')
        if idxh == -1: idxh = 10000
        if idxb == -1: idxb = 10000
        types[i] = t[:min(idxh, idxb)]
    types[i] = types[i].strip()

# create df, write to csv
print('Creating dataframe...')
df = pd.DataFrame(list(zip(names, types, redshifts, ra, dec)), columns = ['name', 'type', 'redshift', 'right ascension', 'declination'])

print(df)

print ('Dropping duplicates...')
df.drop_duplicates()

print('Writing to newdatabase.csv...')
df.to_csv('newdatabase.csv', index=False)

print(f'All done! {changed} cross-matches were found.')

