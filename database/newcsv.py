import pandas as pd
import csv, json

# append the novae from found.json (swifts)
f = open('found.json')
found = json.load(f)
f.close()

names, types = [], []
for i, j in found.items():
    names.append(i)
    types.append(j)
    print(f'Added {i} with type {j}.')


# append the updated.csv names, types
with open('updated.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        if '_dup' in row[0]: continue
        names.append(row[0])
        types.append(row[1])
        print(f'Added {row[0]} with type {row[1]}.')
        
# get PTFs
with open('PTF_CClist.txt', 'r') as ptflist:
    for line in ptflist:
        line = line.split()        
        names.append(line[0])
        types.append(line[1])
        print(f'Added {line[0]} with type {line[1]}.')

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

# search for cross-matches
changed = 0
prefixes = ['ztf', 'ptf', 'iptf', 'atlas', 'dlt', 'gaia', 'asassn', 'pgir']
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
print('Formatting...')
for i, name in enumerate(names):
    if name[:2].lower() == 'sn':
        names[i] = 'SN' + name[2:].lower()
        print(f'{name} was updated to {names[i]}')

print('Creating dataframe...')
df = pd.DataFrame(list(zip(names, types)), columns = ['name', 'type'])

print ('Dropping duplicates...')
df.drop_duplicates()

print('Writing to newdatabase.csv...')
df.to_csv('newdatabase.csv', index=False)

print(f'All done! {changed} cross-matches were found.')

