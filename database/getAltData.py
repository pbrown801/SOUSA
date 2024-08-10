import csv, json


## download from https://www.wis-tns.org/system/files/tns_public_objects/tns_public_objects.csv.zip

names = {}
with open('tns_public_objects.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        names['SN' + row[2]] = row[18].split()
for name in names:
    print(name, names[name])

with open('altnames.json', 'w') as json_file:
    json.dump(names, json_file)
