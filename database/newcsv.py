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

# append the updated.csv names, types
with open('updated.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if '_dup' in row[0]: continue
        names.append(row[0])
        types.append(row[1])

# format names

with open('altnames.json', 'r') as json_file:
    altnames = json.load(json_file)

for i in range(len(names)):
    name = names[i]
    if name[:2].lower() == 'sn' or name[:2].lower() == 'at':
        names[i] = name[:2].upper() + name[2:].lower()
    else:
        for item in altnames:
            if name[:3].lower() == 'ztf':
                if name[:3].upper() + name[3:].lower() in altnames[item]:
                    print(f'{names[i]} is {item}')
                    names[i] = item
                else:
                    names[i] = name[:3].upper() + name[3:].lower()
            if name[:3].lower() == 'dlt':
                if name[:3].upper() + name[3:].lower() in altnames[item]:
                    print(f'{names[i]} is {item}')
                    names[i] = item

        
for i, j in zip(names, types):
    print(f'{i}, type {j}')

df = pd.DataFrame(list(zip(names, types)), columns = ['name', 'type'])
df.drop_duplicates()
df.to_csv('newdatabase.csv', index=False)
print(df)
