import pandas as pd
import csv, json

# append the novae from found.json (swifts)
f = open('found.json')
found = json.load(f)
f.close()

names, types, redshifts = [], [], []
for i, j in found.items():
    names.append(i)
    types.append(j)
    redshifts.append('')
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
        print(f'Added {row[0]} with type {row[1]} and redshift {row[2]}.')
        
# get PTFs
with open('PTF_CClist.txt', 'r') as ptflist:
    for line in ptflist:
        line = line.split()        
        names.append(line[0])
        types.append(line[1])
        redshifts.append(line[2])
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
print(f'{changed} cross-matches found. Formatting...')
for i, name in enumerate(names):
    if name[:2].lower() == 'sn':
        names[i] = 'SN' + name[2:].lower()

# search for missing redshifts
print('Searching for missing redshifts...')
names_shifts = {}
with open('tns.csv', 'r') as tnscsv:
    reader = csv.reader(tnscsv)
    next(reader, None)
    next(reader, None)
    for row in reader:
        print(f'SN{row[0]} -> {row[5]}?')
        names_shifts['SN' + row[2]] = row[5]

for i, name in enumerate(names):
    if redshifts[i] == '':
        try:
            redshifts[i] = names_shifts[name]
            print(f"{name}'s redshift was updated to {names_shifts[name]}.")
        except:
            print(f'No redshift found for {name}.')

# create df, write to csv
print('Creating dataframe...')
df = pd.DataFrame(list(zip(names, types, redshifts)), columns = ['name', 'type', 'redshift'])

print ('Dropping duplicates...')
df.drop_duplicates()

print('Writing to newdatabase.csv...')
df.to_csv('newdatabase.csv', index=False)

print(f'All done! {changed} cross-matches were found.')

