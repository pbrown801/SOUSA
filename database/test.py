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
        names.append(line[1])
        print(f'Added {line[0]} with type {line[1]}.')

# search for cross-matches
with open('altnames.json', 'r') as json_file:
    altnames = json.load(json_file)

prefixes = ['ztf', 'ptf', 'iptf', 'atlas', 'dlt']
for i, name in enumerate(names):
    # skip novae that do not have these prefixes
    if not any(prefix in name[:5].lower() for prefix in prefixes):
        continue
    for item in altnames:
        # search list for cross matches
        if name.lower().strip() in str(altnames[item]).lower():
            print(f'Cross-match successful: {names[i]} was changed to {item}.')
            names[i] = item
            break

print('Creating dataframe...')
df = pd.DataFrame(list(zip(names, types)), columns = ['name', 'type'])

print ('Dropping duplicates...')
df.drop_duplicates()

print('Writing to newdatabase.csv...')
df.to_csv('newdatabase.csv', index=False)

print('All done!')
