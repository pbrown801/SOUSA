import csv, json

names = {}
with open('tns.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        names['SN' + row[2]] = row[18].split()
for name in names:
    print(name, names[name])

with open('altnames.json', 'w') as json_file:
    json.dump(names, json_file)
